#include <pick_place.h>
#include <ros/console.h>
#include <tf_conversions/tf_eigen.h>

const double FINGER_MAX = 6400;

using namespace kinova;


tf::Quaternion EulerZYZ_to_Quaternion(double tz1, double ty, double tz2)
{
    tf::Quaternion q;
    tf::Matrix3x3 rot;
    tf::Matrix3x3 rot_temp;
    rot.setIdentity();

    rot_temp.setEulerYPR(tz1, 0.0, 0.0);
    rot *= rot_temp;
    rot_temp.setEulerYPR(0.0, ty, 0.0);
    rot *= rot_temp;
    rot_temp.setEulerYPR(tz2, 0.0, 0.0);
    rot *= rot_temp;
    rot.getRotation(q);
    return q;
}


PickPlace::PickPlace(ros::NodeHandle &nh):
    nh_(nh)
{
//    if(ros::console::set_logger_level(ROSCONSOLE_DEFAULT_NAME, ros::console::levels::Debug))
//    {
//        ros::console::notifyLoggerLevelsChanged();
//    }

    ros::NodeHandle pn("~");

    nh_.param<std::string>("/robot_type",robot_type_,"j2s7s300");
    nh_.param<bool>("/robot_connected",robot_connected_,true);
    kinova_service = nh_.advertiseService("/kinova_move_srv", &PickPlace::my_pick2, this);
    if (robot_connected_)
    {
        //sub_joint_ = nh_.subscribe<sensor_msgs::JointState>("/j2s7s300_driver/out/joint_state", 1, &PickPlace::get_current_state, this);
        sub_pose_ = nh_.subscribe<geometry_msgs::PoseStamped>("/" + robot_type_ +"_driver/out/tool_pose", 1, &PickPlace::get_current_pose, this);
    }

    // Before we can load the planner, we need two objects, a RobotModel and a PlanningScene.
    robot_model_loader::RobotModelLoader robot_model_loader("robot_description");
    robot_model_ = robot_model_loader.getModel();

    // construct a `PlanningScene` that maintains the state of the world (including the robot).
    planning_scene_.reset(new planning_scene::PlanningScene(robot_model_));
    planning_scene_monitor_.reset(new planning_scene_monitor::PlanningSceneMonitor("robot_description"));

//    //  every time need retrive current robot state, do the following.
//    robot_state::RobotState& robot_state = planning_scene_->getCurrentStateNonConst();
//    const robot_state::JointModelGroup *joint_model_group = robot_state.getJointModelGroup("arm");

    group_ = new moveit::planning_interface::MoveGroupInterface("arm");
    gripper_group_ = new moveit::planning_interface::MoveGroupInterface("gripper");

    group_->setEndEffectorLink(robot_type_ + "_end_effector");

    finger_client_ = new actionlib::SimpleActionClient<kinova_msgs::SetFingersPositionAction>
            ("/" + robot_type_ + "_driver/fingers_action/finger_positions", false);
    while(robot_connected_ && !finger_client_->waitForServer(ros::Duration(5.0))){
      ROS_INFO("Waiting for the finger action server to come up");
    }

    pub_co_ = nh_.advertise<moveit_msgs::CollisionObject>("/collision_object", 10);
    pub_aco_ = nh_.advertise<moveit_msgs::AttachedCollisionObject>("/attached_collision_object", 10);
    pub_planning_scene_diff_ = nh_.advertise<moveit_msgs::PlanningScene>("planning_scene", 1);

    int arm_joint_num = robot_type_[3]-'0';
    joint_names_.resize(arm_joint_num);
    joint_values_.resize(joint_names_.size());
    for (uint i = 0; i<joint_names_.size(); i++)
    {
        joint_names_[i] = robot_type_ + "_joint_" + boost::lexical_cast<std::string>(i+1);
    }

    // set pre-defined joint and pose values.
    define_cartesian_pose();
    define_joint_values();
    define_release();

    // pick process
    
    result_ = false;
    //my_pick();
    while(true){
        sleep(1);
    }
}


PickPlace::~PickPlace()
{
    // shut down pub and subs
    //sub_joint_.shutdown();
    //sub_pose_.shutdown();
    pub_co_.shutdown();
    pub_aco_.shutdown();
    pub_planning_scene_diff_.shutdown();

    // release memory
    delete group_;
    delete gripper_group_;
    delete finger_client_;
}


void PickPlace::get_current_state(const sensor_msgs::JointStateConstPtr &msg)
{
    boost::mutex::scoped_lock lock(mutex_state_);
    current_state_ = *msg;
}

void PickPlace::get_current_pose(const geometry_msgs::PoseStampedConstPtr &msg)
{
    boost::mutex::scoped_lock lock(mutex_pose_);
    current_pose_ = *msg;
}

/**
 * @brief PickPlace::gripper_action
 * @param gripper_rad close for 6400 and open for 0.0
 * @return true is gripper motion reaches the goal
 */
bool PickPlace::gripper_action(double finger_turn)
{
    if(robot_connected_ == false)
    {
        if (finger_turn>0.5*FINGER_MAX)
        {
          gripper_group_->setNamedTarget("Close");
        }
        else
        {
          gripper_group_->setNamedTarget("Open");
        }
        gripper_group_->move();
        return true;
    }

    if (finger_turn < 0)
    {
        finger_turn = 0.0;
    }
    else
    {
        finger_turn = std::min(finger_turn, FINGER_MAX);
    }

    kinova_msgs::SetFingersPositionGoal goal;
    goal.fingers.finger1 = finger_turn;
    goal.fingers.finger2 = goal.fingers.finger1;
    goal.fingers.finger3 = goal.fingers.finger1;
    finger_client_->sendGoal(goal);

    if (finger_client_->waitForResult(ros::Duration(5.0)))
    {
        finger_client_->getResult();
        return true;
    }
    else
    {
        finger_client_->cancelAllGoals();
        ROS_WARN_STREAM("The gripper action timed-out");
        return false;
    }
}


void PickPlace::clear_workscene()
{
    // remove table
    co_.id = "table";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);

    // remove desk
    co1_.id = "desk";
    co1_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);

    // remove target
    co_.id = "target_cylinder";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);

    //remove attached target
    aco_.object.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_aco_.publish(aco_);

    planning_scene_msg_.world.collision_objects.clear();
    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);

    clear_obstacle();
}

void PickPlace::build_workscene()
{  
    /*
    co_.header.frame_id = "root";
    co_.header.stamp = ros::Time::now();

    // remove table
    co_.id = "table";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);


        // add table
    co_.primitives.resize(1);
    co_.primitive_poses.resize(1);
    co_.primitives[0].type = shape_msgs::SolidPrimitive::BOX;
    co_.primitives[0].dimensions.resize(geometric_shapes::SolidPrimitiveDimCount<shape_msgs::SolidPrimitive::BOX>::value);
    co_.operation = moveit_msgs::CollisionObject::ADD;

    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_X] = 2.4;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Y] = 2.4;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Z] = 0.03;
    co_.primitive_poses[0].position.x = 0;
    co_.primitive_poses[0].position.y = 0.0;
    co_.primitive_poses[0].position.z = -0.1;
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);
    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);
    ros::WallDuration(0.1).sleep();
*/
    co1_.header.frame_id = "root";
    co1_.header.stamp = ros::Time::now();

    // remove table
    co1_.id = "desk";
    co1_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co1_);


    // add scrivania
    co1_.primitives.resize(1);
    co1_.primitive_poses.resize(1);
    co1_.primitives[0].type = shape_msgs::SolidPrimitive::BOX;
    co1_.primitives[0].dimensions.resize(geometric_shapes::SolidPrimitiveDimCount<shape_msgs::SolidPrimitive::BOX>::value);
    co1_.operation = moveit_msgs::CollisionObject::ADD;

    co1_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_X] = 0.05;
    co1_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Y] = 1;
    co1_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Z] = 1.2;
    co1_.primitive_poses[0].position.x = -0.25;
    co1_.primitive_poses[0].position.y = 0.0;
    co1_.primitive_poses[0].position.z = 0.5;
    pub_co_.publish(co1_);
    planning_scene_msg_.world.collision_objects.push_back(co1_);
    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);
    ros::WallDuration(0.1).sleep();
    
    }

void PickPlace::clear_obstacle()
{
    co_.id = "pole";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);

    co_.id = "bot_obstacle";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);

    co_.id = "top_obstacle";
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);

    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);
    ros::WallDuration(0.1).sleep();
    //      ROS_WARN_STREAM(__PRETTY_FUNCTION__ << ": LINE " << __LINE__ << ": remove pole ");
    //      std::cin >> pause_;
}

void PickPlace::add_obstacle()
{
    clear_obstacle();

    co_.id = "pole";
    co_.primitives.resize(1);
    co_.primitive_poses.resize(1);
    co_.primitives[0].type = shape_msgs::SolidPrimitive::BOX;
    co_.primitives[0].dimensions.resize(geometric_shapes::SolidPrimitiveDimCount<shape_msgs::SolidPrimitive::BOX>::value);
    co_.operation = moveit_msgs::CollisionObject::ADD;

    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_X] = 0.1;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Y] = 0.1;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Z] = 0.1;

    co_.primitive_poses[0].position.x = 0.2;
    co_.primitive_poses[0].position.y = 0.0;
    co_.primitive_poses[0].position.z = 0.3;

    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);

    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);
    ros::WallDuration(0.1).sleep();
}

void PickPlace::add_complex_obstacle()
{
    clear_obstacle();

    // add obstacle between robot and object
    co_.id = "bot_obstacle";
    co_.primitives.resize(1);
    co_.primitive_poses.resize(1);
    co_.primitives[0].type = shape_msgs::SolidPrimitive::BOX;
    co_.primitives[0].dimensions.resize(geometric_shapes::SolidPrimitiveDimCount<shape_msgs::SolidPrimitive::BOX>::value);
    co_.operation = moveit_msgs::CollisionObject::ADD;

    double box_h = 0.2;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_X] = 2.4;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Y] = 0.1;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::BOX_Z] = box_h;

    co_.primitive_poses[0].position.x = 0;
    co_.primitive_poses[0].position.y = 0.3;
    co_.primitive_poses[0].position.z = box_h/2.0;
    co_.primitive_poses[0].orientation.w = 1.0;
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);

    co_.id = "top_obstacle";
    co_.primitive_poses[0].position.z = box_h/2.0 + box_h + 0.4;
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);

    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);
    ros::WallDuration(0.1).sleep();
    //      ROS_WARN_STREAM(__PRETTY_FUNCTION__ << ": LINE " << __LINE__ << ": ADD pole ");
    //      std::cin >> pause_;
}

void PickPlace::add_attached_obstacle()
{
    //once the object is know to be grasped
    //we remove obstacle from work scene
    co_.id = "target_cylinder";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);

    //and then we declare it as an attached obstacle
    aco_.object.operation = moveit_msgs::CollisionObject::ADD;
    aco_.link_name = robot_type_ + "_end_effector";
    aco_.touch_links.push_back(robot_type_ + "_end_effector");
    aco_.touch_links.push_back(robot_type_ + "_link_finger_1");
    aco_.touch_links.push_back(robot_type_ + "_link_finger_2");
    aco_.touch_links.push_back(robot_type_ + "_link_finger_3");
    aco_.touch_links.push_back(robot_type_ + "_link_finger_tip_1");
    aco_.touch_links.push_back(robot_type_ + "_link_finger_tip_2");
    aco_.touch_links.push_back(robot_type_ + "_link_finger_tip_3");
    pub_aco_.publish(aco_);
}

void PickPlace::add_target()
{
    //remove target_cylinder
    co_.id = "target_cylinder";
    co_.operation = moveit_msgs::CollisionObject::REMOVE;
    pub_co_.publish(co_);

    //add target_cylinder
    co_.primitives.resize(1);
    co_.primitive_poses.resize(1);
    co_.primitives[0].type = shape_msgs::SolidPrimitive::CYLINDER;
    co_.primitives[0].dimensions.resize(geometric_shapes::SolidPrimitiveDimCount<shape_msgs::SolidPrimitive::CYLINDER>::value);
    co_.operation = moveit_msgs::CollisionObject::ADD;

    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::CYLINDER_HEIGHT] = 0.5;
    co_.primitives[0].dimensions[shape_msgs::SolidPrimitive::CYLINDER_RADIUS] = 0.04;
    co_.primitive_poses[0].position.x = 0.0;
    co_.primitive_poses[0].position.y = 0.6;
    co_.primitive_poses[0].position.z = 0.3;
    can_pose_.pose.position.x = co_.primitive_poses[0].position.x;
    can_pose_.pose.position.y = co_.primitive_poses[0].position.y;
    can_pose_.pose.position.z = co_.primitive_poses[0].position.z;
    pub_co_.publish(co_);
    planning_scene_msg_.world.collision_objects.push_back(co_);
    planning_scene_msg_.is_diff = true;
    pub_planning_scene_diff_.publish(planning_scene_msg_);
    aco_.object = co_;
    ros::WallDuration(0.1).sleep();
}

void PickPlace::check_collision()
{
    collision_detection::CollisionRequest collision_request;
    collision_detection::CollisionResult collision_result;
    collision_request.contacts = true;
    collision_request.max_contacts = 1000;

    collision_result.clear();
    planning_scene_->checkCollision(collision_request, collision_result);
    ROS_INFO_STREAM("Test 1: Current state is "
                    << (collision_result.collision ? "in" : "not in")
                    << " collision");

    collision_request.group_name = "arm";
    collision_result.clear();
    planning_scene_->checkCollision(collision_request, collision_result);
    ROS_INFO_STREAM("Test 3: Current state is "
                    << (collision_result.collision ? "in" : "not in")
                    << " collision");

    // check contact
    planning_scene_->checkCollision(collision_request, collision_result);
    ROS_INFO_STREAM("Test 4: Current state is "
                    << (collision_result.collision ? "in" : "not in")
                    << " collision");
    collision_detection::CollisionResult::ContactMap::const_iterator it;
    for(it = collision_result.contacts.begin();
        it != collision_result.contacts.end();
        ++it)
    {
        ROS_INFO("Contact between: %s and %s",
                 it->first.first.c_str(),
                 it->first.second.c_str());
    }

    // allowed collision matrix
    collision_detection::AllowedCollisionMatrix acm = planning_scene_->getAllowedCollisionMatrix();
    robot_state::RobotState copied_state = planning_scene_->getCurrentState();

    collision_detection::CollisionResult::ContactMap::const_iterator it2;
    for(it2 = collision_result.contacts.begin();
        it2 != collision_result.contacts.end();
        ++it2)
    {
        acm.setEntry(it2->first.first, it2->first.second, true);
    }
    collision_result.clear();
    planning_scene_->checkCollision(collision_request, collision_result, copied_state, acm);
    ROS_INFO_STREAM("Test 5: Current state is "
                    << (collision_result.collision ? "in" : "not in")
                    << " collision");
}


void PickPlace::define_cartesian_pose()
{
    tf::Quaternion q;

    // define start pose before grasp
    start_pose_.header.frame_id = "root";
    start_pose_.header.stamp = ros::Time::now();
    start_pose_.pose.position.x = 0.5;
    start_pose_.pose.position.y = -0.5;
    start_pose_.pose.position.z = 0.5;

    q = EulerZYZ_to_Quaternion(-M_PI/4, M_PI/2, M_PI);
    start_pose_.pose.orientation.x = q.x();
    start_pose_.pose.orientation.y = q.y();
    start_pose_.pose.orientation.z = q.z();
    start_pose_.pose.orientation.w = q.w();

    // define grasp pose
    grasp_pose_human_1.header.frame_id = "root";
    grasp_pose_human_1.header.stamp  = ros::Time::now();

    grasp_pose_human_0.header.frame_id = "root";
    grasp_pose_human_0.header.stamp  = ros::Time::now();

    grasp_pose_robot_1.header.frame_id = "root";
    grasp_pose_robot_0.header.stamp  = ros::Time::now();

    grasp_pose_robot_1.header.frame_id = "root";
    grasp_pose_robot_0.header.stamp  = ros::Time::now();

    // Euler_ZYZ (-M_PI/4, M_PI/2, M_PI/2)
    //human0

    grasp_pose_human_0.pose.position.x = 0.55;//0.0;
    grasp_pose_human_0.pose.position.y = -0.2;//0.6;
    grasp_pose_human_0.pose.position.z = 0.03; //0.3;


    grasp_pose_human_1.pose.position.x = 0.55;//0.0;
    grasp_pose_human_1.pose.position.y = 0.2;//0.6;
    grasp_pose_human_1.pose.position.z = 0.03; //0.3;


    grasp_pose_robot_0.pose.position.x = 0.40;//0.0;
    grasp_pose_robot_0.pose.position.y = -0.2;//0.6;
    grasp_pose_robot_0.pose.position.z = 0.03; //0.3;

    grasp_pose_robot_1.pose.position.x = 0.40;//0.0;
    grasp_pose_robot_1.pose.position.y = 0.2;//0.6;
    grasp_pose_robot_1.pose.position.z = 0.03; //0.3;

    q = EulerZYZ_to_Quaternion(M_PI, M_PI, 0);
    grasp_pose_human_0.pose.orientation.x = q.x();
    grasp_pose_human_0.pose.orientation.y = q.y();
    grasp_pose_human_0.pose.orientation.z = q.z();
    grasp_pose_human_0.pose.orientation.w = q.w();

    grasp_pose_human_1.pose.orientation.x = q.x();
    grasp_pose_human_1.pose.orientation.y = q.y();
    grasp_pose_human_1.pose.orientation.z = q.z();
    grasp_pose_human_1.pose.orientation.w = q.w();

    grasp_pose_robot_0.pose.orientation.x = q.x();
    grasp_pose_robot_0.pose.orientation.y = q.y();
    grasp_pose_robot_0.pose.orientation.z = q.z();
    grasp_pose_robot_0.pose.orientation.w = q.w();

    grasp_pose_robot_1.pose.orientation.x = q.x();
    grasp_pose_robot_1.pose.orientation.y = q.y();
    grasp_pose_robot_1.pose.orientation.z = q.z();
    grasp_pose_robot_1.pose.orientation.w = q.w();


    // define release
    release_1.header.frame_id = "root";
    release_1.header.stamp  = ros::Time::now();

    release_2.header.frame_id = "root";
    release_2.header.stamp  = ros::Time::now();


    release_3.header.frame_id = "root";
    release_3.header.stamp  = ros::Time::now();

    release_4.header.frame_id = "root";
    release_4.header.stamp  = ros::Time::now();



    // Euler_ZYZ (-M_PI/4, M_PI/2, M_PI/2)
    //human0
    release_1.pose.position.x = 0.10;
    release_1.pose.position.y = -0.55;
    release_1.pose.position.z = 0.03;

    release_2.pose.position.x = -0.10;
    release_2.pose.position.y = -0.55;
    release_2.pose.position.z = 0.03;

    release_3.pose.position.x = 0.10;
    release_3.pose.position.y = -0.73;
    release_3.pose.position.z = 0.03;

    release_4.pose.position.x = -0.10;
    release_4.pose.position.y = -0.73;
    release_4.pose.position.z = 0.03;


    q = EulerZYZ_to_Quaternion(M_PI, M_PI, 0);
    release_1.pose.orientation.x = q.x();
    release_1.pose.orientation.y = q.y();
    release_1.pose.orientation.z = q.z();
    release_1.pose.orientation.w = q.w();

    release_2.pose.orientation.x = q.x();
    release_2.pose.orientation.y = q.y();
    release_2.pose.orientation.z = q.z();
    release_2.pose.orientation.w = q.w();

    release_3.pose.orientation.x = q.x();
    release_3.pose.orientation.y = q.y();
    release_3.pose.orientation.z = q.z();
    release_3.pose.orientation.w = q.w();

    release_4.pose.orientation.x = q.x();
    release_4.pose.orientation.y = q.y();
    release_4.pose.orientation.z = q.z();
    release_4.pose.orientation.w = q.w();
    // generate_pregrasp_pose(double dist, double azimuth, double polar, double rot_gripper_z)
    /*
    grasp_pose_= generate_gripper_align_pose(grasp_pose_, 0.03999, 0, 0, M_PI);
    pregrasp_pose_ = generate_gripper_align_pose(grasp_pose_, 0.1, 0, 0, M_PI);
    postgrasp_pose_ = grasp_pose_;
    postgrasp_pose_.pose.position.z = grasp_pose_.pose.position.z + 0.05;*/

}

void PickPlace::define_joint_values()
{
    start_joint_.resize(joint_names_.size());
    //    getInvK(start_pose_, start_joint_);
    start_joint_[0] = 234.4 *M_PI/180.0;
    start_joint_[1] = 256.0 *M_PI/180.0;
    start_joint_[2] = 91.4 *M_PI/180.0;
    start_joint_[3] = 163.4 *M_PI/180.0;
    start_joint_[4] = 88.5 *M_PI/180.0;
    start_joint_[5] = 151.0 *M_PI/180.0;


    grasp_joint_robot_0.resize(joint_names_.size());
    grasp_joint_robot_0[0] = 20 *M_PI/180.0;
    grasp_joint_robot_0[1] = 120 *M_PI/180.0;
    grasp_joint_robot_0[2] = 180 *M_PI/180.0;
    grasp_joint_robot_0[3] = 105 *M_PI/180.0;
    grasp_joint_robot_0[4] = 180 *M_PI/180.0;
    grasp_joint_robot_0[5] = 130 *M_PI/180.0;
    grasp_joint_robot_0[6] = -167 *M_PI/180.0;

    pregrasp_joint_robot_0.resize(joint_names_.size());
    pregrasp_joint_robot_0[0] = 20 *M_PI/180.0;
    pregrasp_joint_robot_0[1] = 130 *M_PI/180.0;
    pregrasp_joint_robot_0[2] = 180 *M_PI/180.0;
    pregrasp_joint_robot_0[3] = 150 *M_PI/180.0;
    pregrasp_joint_robot_0[4] = 180 *M_PI/180.0;
    pregrasp_joint_robot_0[5] = 130 *M_PI/180.0;
    pregrasp_joint_robot_0[6] = -167 *M_PI/180.0;


    grasp_joint_robot_1.resize(joint_names_.size());
    grasp_joint_robot_1[0] = 0 *M_PI/180.0;
    grasp_joint_robot_1[1] = 120 *M_PI/180.0;
    grasp_joint_robot_1[2] = 180 *M_PI/180.0;
    grasp_joint_robot_1[3] = 105 *M_PI/180.0;
    grasp_joint_robot_1[4] = 180 *M_PI/180.0;
    grasp_joint_robot_1[5] = 130 *M_PI/180.0;
    grasp_joint_robot_1[6] = -167 *M_PI/180.0;

    pregrasp_joint_robot_1.resize(joint_names_.size());
    pregrasp_joint_robot_1[0] = 0 *M_PI/180.0;
    pregrasp_joint_robot_1[1] = 130 *M_PI/180.0;
    pregrasp_joint_robot_1[2] = 180 *M_PI/180.0;
    pregrasp_joint_robot_1[3] = 140 *M_PI/180.0;
    pregrasp_joint_robot_1[4] = 180 *M_PI/180.0;
    pregrasp_joint_robot_1[5] = 130 *M_PI/180.0;
    pregrasp_joint_robot_1[6] = -167 *M_PI/180.0;



    grasp_joint_human_0.resize(joint_names_.size());
    grasp_joint_human_0[0] = 20 *M_PI/180.0;
    grasp_joint_human_0[1] = 85 *M_PI/180.0;
    grasp_joint_human_0[2] = 180 *M_PI/180.0;
    grasp_joint_human_0[3] = 180 *M_PI/180.0;
    grasp_joint_human_0[4] = 180 *M_PI/180.0;
    grasp_joint_human_0[5] = 90 *M_PI/180.0;
    grasp_joint_human_0[6] = -167 *M_PI/180.0;


    pregrasp_joint_human_0.resize(joint_names_.size());
    pregrasp_joint_human_0[0] = 20 *M_PI/180.0;
    pregrasp_joint_human_0[1] = 130 *M_PI/180.0;
    pregrasp_joint_human_0[2] = 180 *M_PI/180.0;
    pregrasp_joint_human_0[3] = 180 *M_PI/180.0;
    pregrasp_joint_human_0[4] = 180 *M_PI/180.0;
    pregrasp_joint_human_0[5] = 90 *M_PI/180.0;
    pregrasp_joint_human_0[6] = -167 *M_PI/180.0;


    grasp_joint_human_1.resize(joint_names_.size());
    grasp_joint_human_1[0] = 0 *M_PI/180.0;
    grasp_joint_human_1[1] = 83 *M_PI/180.0;
    grasp_joint_human_1[2] = 180 *M_PI/180.0;
    grasp_joint_human_1[3] = 180 *M_PI/180.0;
    grasp_joint_human_1[4] = 180 *M_PI/180.0;
    grasp_joint_human_1[5] = 90 *M_PI/180.0;
    grasp_joint_human_1[6] = -167 *M_PI/180.0;


    pregrasp_joint_human_1.resize(joint_names_.size());
    pregrasp_joint_human_1[0] = 0 *M_PI/180.0;
    pregrasp_joint_human_1[1] = 130 *M_PI/180.0;
    pregrasp_joint_human_1[2] = 180 *M_PI/180.0;
    pregrasp_joint_human_1[3] = 180 *M_PI/180.0;
    pregrasp_joint_human_1[4] = 180 *M_PI/180.0;
    pregrasp_joint_human_1[5] = 90 *M_PI/180.0;
    pregrasp_joint_human_1[6] = -167 *M_PI/180.0;

    pregrasp_joint_.resize(joint_names_.size());
    pregrasp_joint_[0] = 0 *M_PI/180.0;
    pregrasp_joint_[1] = 121 *M_PI/180.0;
    pregrasp_joint_[2] = 180 *M_PI/180.0;
    pregrasp_joint_[3] = 182 *M_PI/180.0;
    pregrasp_joint_[4] = 180 *M_PI/180.0;
    pregrasp_joint_[5] = 93*M_PI/180.0;
    pregrasp_joint_[6] = -167 *M_PI/180.0;
 
}


void PickPlace::define_release()
{
    release_joint_4.resize(joint_names_.size());
    release_joint_4[0] = 103 *M_PI/180.0;
    release_joint_4[1] = 90 *M_PI/180.0;//90!
    release_joint_4[2] = 180 *M_PI/180.0;
    release_joint_4[3] = 180 *M_PI/180.0;
    release_joint_4[4] = 180 *M_PI/180.0;
    release_joint_4[5] = 90 *M_PI/180.0;
    release_joint_4[6] = -167 *M_PI/180.0;

    release_joint_3.resize(joint_names_.size());
    release_joint_3[0] = 85 *M_PI/180.0;
    release_joint_3[1] = 90 *M_PI/180.0;
    release_joint_3[2] = 180 *M_PI/180.0;
    release_joint_3[3] = 180 *M_PI/180.0;
    release_joint_3[4] = 180 *M_PI/180.0;
    release_joint_3[5] = 90 *M_PI/180.0;
    release_joint_3[6] = -167 *M_PI/180.0;

    release_joint_1.resize(joint_names_.size());
    release_joint_1[0] = 85 *M_PI/180.0;
    release_joint_1[1] = 125 *M_PI/180.0;//125
    release_joint_1[2] = 180 *M_PI/180.0;
    release_joint_1[3] = 90 *M_PI/180.0;
    release_joint_1[4] = 180 *M_PI/180.0;
    release_joint_1[5] = 130*M_PI/180.0;
    release_joint_1[6] = -167 *M_PI/180.0;

    release_joint_2.resize(joint_names_.size());
    release_joint_2[0] = 105 *M_PI/180.0;
    release_joint_2[1] = 125 *M_PI/180.0;
    release_joint_2[2] = 180 *M_PI/180.0;
    release_joint_2[3] = 90 *M_PI/180.0;
    release_joint_2[4] = 180 *M_PI/180.0;
    release_joint_2[5] = 130*M_PI/180.0;
    release_joint_2[6] = -167 *M_PI/180.0;

    prerelease_joint_.resize(joint_names_.size());
    prerelease_joint_[0] = 90 *M_PI/180.0;
    prerelease_joint_[1] = 130 *M_PI/180.0;
    prerelease_joint_[2] = 180 *M_PI/180.0;
    prerelease_joint_[3] = 139 *M_PI/180.0;
    prerelease_joint_[4] = 180 *M_PI/180.0;
    prerelease_joint_[5] = 130*M_PI/180.0;
    prerelease_joint_[6] = -167 *M_PI/180.0;
 
}

/**
 * @brief PickPlace::generate_gripper_align_pose
 * @param targetpose_msg pick/place pose (object location): where gripper close/open the fingers (grasp/release the object). Only position information is used.
 * @param dist distance of returned pose to targetpose
 * @param azimuth an angle measured from the x-axis in the xy-plane in spherical coordinates, denoted theta (0<= theta < 2pi ).
 * @param polar also named zenith, colatitude, denoted phi (0<=phi<=pi). It is the angle from the positive z-axis to the vector.  phi= pi/2 - delta where delta is the latitude.
 * @param rot_gripper_z rotation along the z axis of the gripper reference frame (last joint rotation)
 * @return a pose defined in a spherical coordinates where origin is located at the target pose. Normally it is a pre_grasp/post_realease pose, where gripper axis (last joint axis) is pointing to the object (target_pose).
 */
geometry_msgs::PoseStamped PickPlace::generate_gripper_align_pose(geometry_msgs::PoseStamped targetpose_msg, double dist, double azimuth, double polar, double rot_gripper_z)
{
    geometry_msgs::PoseStamped pose_msg;

    pose_msg.header.frame_id = "root";

    // computer pregrasp position w.r.t. location of grasp_pose in spherical coordinate. Orientation is w.r.t. fixed world (root) reference frame.
    double delta_x = -dist * cos(azimuth) * sin(polar);
    double delta_y = -dist * sin(azimuth) * sin(polar);
    double delta_z = -dist * cos(polar);

    // computer the orientation of gripper w.r.t. fixed world (root) reference frame. The gripper (z axis) should point(open) to the grasp_pose.
    tf::Quaternion q = EulerZYZ_to_Quaternion(azimuth, polar, rot_gripper_z);

    pose_msg.pose.position.x = targetpose_msg.pose.position.x + delta_x;
    pose_msg.pose.position.y = targetpose_msg.pose.position.y + delta_y;
    pose_msg.pose.position.z = targetpose_msg.pose.position.z + delta_z;
    pose_msg.pose.orientation.x = q.x();
    pose_msg.pose.orientation.y = q.y();
    pose_msg.pose.orientation.z = q.z();
    pose_msg.pose.orientation.w = q.w();

    ROS_DEBUG_STREAM(__PRETTY_FUNCTION__ << ": LINE: " << __LINE__ << ": " << "pose_msg: x " << pose_msg.pose.position.x  << ", y " << pose_msg.pose.position.y  << ", z " << pose_msg.pose.position.z  << ", qx " << pose_msg.pose.orientation.x  << ", qy " << pose_msg.pose.orientation.y  << ", qz " << pose_msg.pose.orientation.z  << ", qw " << pose_msg.pose.orientation.w );

    return pose_msg;

}


void PickPlace::setup_constrain(geometry_msgs::Pose target_pose, bool orientation, bool position)
{

}

void PickPlace::check_constrain()
{
    moveit_msgs::Constraints grasp_constrains = group_->getPathConstraints();
    bool has_constrain = false;
    ROS_INFO("check constrain result: ");
    if (!grasp_constrains.orientation_constraints.empty())
    {
        has_constrain = true;
        ROS_INFO("Has orientation constrain. ");
    }
    if(!grasp_constrains.position_constraints.empty())
    {
        has_constrain = true;
        ROS_INFO("Has position constrain. ");
    }
    if(has_constrain == false)
    {
        ROS_INFO("No constrain. ");
    }
}

void PickPlace::evaluate_plan(moveit::planning_interface::MoveGroupInterface &group)
{
    bool replan = true;
    int count = 0;

    moveit::planning_interface::MoveGroupInterface::Plan my_plan;

    while (replan == true && ros::ok())
    {
        // reset flag for replan
        count = 0;
        result_ = false;

        // try to find a success plan.
        double plan_time;
        while (result_ == false && count < 5)
        {
            count++;
            plan_time = 20+count*10;
            ROS_INFO("Setting plan time to %f sec", plan_time);
            group.setPlanningTime(plan_time);
            result_ = (group.plan(my_plan) == moveit_msgs::MoveItErrorCodes::SUCCESS);
            std::cout << "at attemp: " << count << std::endl;
            ros::WallDuration(0.1).sleep();
        }

        // found a plan
        if (result_ == true)
        {
            std::cout << "plan success at attemp: " << count << std::endl;

            replan = false;
            /*
            std::cout << "please input e to execute the plan, r to replan, others to skip: ";
            std::cin >> pause_;
            ros::WallDuration(0.5).sleep();
            if (pause_ == "r" || pause_ == "R" )
            {
                replan = true;
            }
            else
            {
                replan = false;
            }*/
        }
        else // not found
        {
            std::cout << "Exit since plan failed until reach maximum attemp: " << count << std::endl;
            replan = false;
            break;
        }
    }
    std::cout <<result_ << std::endl;
    if(result_ == true)
    {
       // pause_ == "e";
       // if (pause_ == "e" || pause_ == "E")
       // {
             std::cout <<"result_ "<< std::endl;
            group.execute(my_plan);
        //}
    }
    ros::WallDuration(1.0).sleep();
}


bool PickPlace::my_pick()
{

    return true;
   
}

bool PickPlace::my_pick2(pp_task::MoveArm::Request &req, pp_task::MoveArm::Response &res)
{

    ROS_INFO_STREAM("I AM HERE");
    int block=req.block;
    double vel=req.speed;
    clear_workscene();
    ros::WallDuration(1.0).sleep();
    build_workscene();
    ros::WallDuration(1.0).sleep();
    group_->setMaxVelocityScalingFactor(vel);
    group_->setMaxAccelerationScalingFactor(vel);

    if (req.block_owner=="home"){
    ROS_INFO_STREAM("GOING HOME");
    group_->clearPathConstraints();
    group_->setNamedTarget("Home");
    evaluate_plan(*group_);
    }
    else if (req.block_owner=="random"){
     ROS_INFO_STREAM("GOING HOME");
    group_->clearPathConstraints();
    group_->setRandomTarget();
    evaluate_plan(*group_);
    }
    else{

    ROS_INFO_STREAM("GOING HOME");
    group_->clearPathConstraints();
    group_->setNamedTarget("Home");
    evaluate_plan(*group_);

    ros::WallDuration(1.0).sleep();
    gripper_group_->setNamedTarget("Open");
    gripper_group_->move();

    //add_obstacle();
    //clear_workscene();

    
    if (req.block_owner=="human"){
    if (block==0){

    ROS_INFO_STREAM("GOING PREGRASP");
    if (req.amplitude=="high"){
        pregrasp_joint_human_0[1]=pregrasp_joint_human_0[1]+5*M_PI/180.0;
    }
    else if (req.amplitude=="low"){
        pregrasp_joint_human_0[1]=pregrasp_joint_human_0[1]-5*M_PI/180.0;
    }
    group_->setJointValueTarget(pregrasp_joint_human_0);
    evaluate_plan(*group_);
    ROS_INFO_STREAM("GRASP");
    group_->setJointValueTarget(grasp_joint_human_0);
    evaluate_plan(*group_);
    ROS_INFO_STREAM("CLOSE HAND");
    gripper_action(0.75*FINGER_MAX); // partially close
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_human_0);
    evaluate_plan(*group_);
    }
    else if (block==1){
    if (req.amplitude=="high"){
        pregrasp_joint_human_1[1]=pregrasp_joint_human_1[1]+5*M_PI/180.0;
    }
    else if (req.amplitude=="low"){
        pregrasp_joint_human_1[1]=pregrasp_joint_human_1[1]-5*M_PI/180.0;
    }
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_human_1);
    evaluate_plan(*group_);
    ROS_INFO_STREAM("GRASP");
    group_->setJointValueTarget(grasp_joint_human_1);
    evaluate_plan(*group_);
    ROS_INFO_STREAM("CLOSE HAND");
    gripper_action(0.75*FINGER_MAX); // partially close
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_human_1);
    evaluate_plan(*group_);
    }
    }
    else if (req.block_owner=="robot"){
    if (block==0){
    if (req.amplitude=="high"){
        pregrasp_joint_robot_0[1]=pregrasp_joint_robot_0[1]+5*M_PI/180.0;
    }
    else if (req.amplitude=="low"){
        pregrasp_joint_robot_0[1]=pregrasp_joint_robot_0[1]-5*M_PI/180.0;
    }
    ROS_INFO_STREAM("ROBOT BLOCK 0");
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_robot_0);
    evaluate_plan(*group_);

    ROS_INFO_STREAM("GRASP");
    group_->setJointValueTarget(grasp_joint_robot_0);
    evaluate_plan(*group_);
    ROS_INFO_STREAM("CLOSE HAND");
    gripper_action(0.75*FINGER_MAX); // partially close
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_robot_0);
    evaluate_plan(*group_);
    }
    else if (block==1){

    if (req.amplitude=="high"){
        pregrasp_joint_robot_1[1]=pregrasp_joint_robot_1[1]+5*M_PI/180.0;
    }
    else if (req.amplitude=="low"){
        pregrasp_joint_robot_1[1]=pregrasp_joint_robot_1[1]-5*M_PI/180.0;
    }
    ROS_INFO_STREAM("ROBOT BLOCK 1");
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_robot_1);
    evaluate_plan(*group_);

    ROS_INFO_STREAM("GRASP");
    group_->setJointValueTarget(grasp_joint_robot_1);
    evaluate_plan(*group_);
    ROS_INFO_STREAM("CLOSE HAND");
    gripper_action(0.75*FINGER_MAX); // partially close
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(pregrasp_joint_robot_1);
    evaluate_plan(*group_);

    }}
    

    if (req.amplitude=="high"){
        prerelease_joint_[1]=prerelease_joint_[1]+5*M_PI/180.0;
    }
    else if (req.amplitude=="low"){
        prerelease_joint_[1]=prerelease_joint_[1]-5*M_PI/180.0;
    }
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(prerelease_joint_);
    evaluate_plan(*group_);

    if(req.final_pose=="area1"){
    ROS_INFO_STREAM("GOING RELEASE");
    if(req.style=="wrong"){
        release_joint_1[0]=release_joint_1[0]-10*M_PI/180.0;
    }
    group_->setJointValueTarget(release_joint_1);
    evaluate_plan(*group_);
    }
    else if(req.final_pose=="area2"){
    ROS_INFO_STREAM("GOING RELEASE");
    if(req.style=="wrong"){
        release_joint_2[0]=release_joint_2[0]-10*M_PI/180.0;
    }
    group_->setJointValueTarget(release_joint_2);
    evaluate_plan(*group_);
    }

    else if(req.final_pose=="area3"){
    ROS_INFO_STREAM("GOING RELEASE");
    if(req.style=="wrong"){
        release_joint_3[0]=release_joint_3[0]-10*M_PI/180.0;
    }
    group_->setJointValueTarget(release_joint_3);
    evaluate_plan(*group_);
    }
    else if(req.final_pose=="area4"){
    ROS_INFO_STREAM("GOING RELEASE");
    if(req.style=="wrong"){
        release_joint_4[0]=release_joint_4[0]-10*M_PI/180.0;
    }
    group_->setJointValueTarget(release_joint_4);
    evaluate_plan(*group_);
    }
    ROS_INFO_STREAM("OPEN HAND");
    gripper_action(0.0); // full open
    ROS_INFO_STREAM("GOING PREGRASP");
    group_->setJointValueTarget(prerelease_joint_);
    evaluate_plan(*group_);



    ROS_INFO_STREAM("GOING HOME");
    group_->clearPathConstraints();
    group_->setNamedTarget("Home");
    evaluate_plan(*group_);
    define_release();
    }
   return true;
    
}

void PickPlace::getInvK(geometry_msgs::Pose &eef_pose, std::vector<double> &joint_value)
{
    // TODO: transform cartesian command to joint space, and alway motion plan in joint space.
}


int main(int argc, char **argv)
{
    ros::init(argc, argv, "pick_place_demo");
    ros::NodeHandle node;
    ros::AsyncSpinner spinner(2);
    spinner.start();
    kinova::PickPlace pick_place(node);


    return 0;
}
