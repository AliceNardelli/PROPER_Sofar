#include "ros/ros.h"
#include <iostream>
#include <dlfcn.h> //Ubuntu
#include <KinovaTypes.h>
#include <Kinova.API.CommLayerUbuntu.h>
#include<unistd.h> 
#include <cmath> 
#include <pp_task/MoveArm.h>
#include "geometry_msgs/PoseStamped.h"
#include <cstdlib>
//Note that under windows, you may/will have to perform other #include


int (*MyInitAPI)();
int (*MyCloseAPI)();
int (*MySetActuatorPID)(unsigned int address, float P, float I, float D);
int (*MySendAdvanceTrajectory)(TrajectoryPoint command);
int (*MyStartControlAPI)();
int (*MyGetCartesianPosition)(CartesianPosition &);
ros::Publisher pose_pub;



TrajectoryPoint define_limitations(int acc, int vel, TrajectoryPoint trajectoryPoint){
                float P = 0.5; 
                float I = 0.0; 
                float D = 0.05;
                trajectoryPoint.Limitations.accelerationParameter1 = 0.0f; 
                trajectoryPoint.Limitations.accelerationParameter2 = 0.0f; 
                trajectoryPoint.Limitations.accelerationParameter3 = 0.0f;
                if (acc==1){
                float P = 2; 
                float I = 0.01;
                float D = 0.05;
                trajectoryPoint.Limitations.accelerationParameter1 = 1.0f; 
                trajectoryPoint.Limitations.accelerationParameter2 = 1.0f;
                trajectoryPoint.Limitations.accelerationParameter3 = 1.0f; 
                }
                for(int i=0; i<8; i++){             
                (*MySetActuatorPID)(i, P, I, D);}
                trajectoryPoint.Limitations.forceParameter1 = 0.0f;  
                trajectoryPoint.Limitations.forceParameter2 = 0.0f;  
                trajectoryPoint.Limitations.forceParameter3 = 0.0f; 
                if(vel==0){
                trajectoryPoint.Limitations.speedParameter1 = 0.05f;
                trajectoryPoint.Limitations.speedParameter2 = 0.2f; 
                trajectoryPoint.Limitations.speedParameter3 = 0.05f;
                }
                else if(vel==1){
                trajectoryPoint.Limitations.speedParameter1 = 0.09f;
                trajectoryPoint.Limitations.speedParameter2 = 0.5f; 
                trajectoryPoint.Limitations.speedParameter3 = 0.09f;
                }
                else{
                trajectoryPoint.Limitations.speedParameter1 = 0.2f;
                trajectoryPoint.Limitations.speedParameter2 = 1.0f; 
                trajectoryPoint.Limitations.speedParameter3 = 0.2f;  
                }
                trajectoryPoint.LimitationsActive = 1;
                return trajectoryPoint;
}






bool kinova_motion_srv(pp_task::MoveArm::Request  &req,
         pp_task::MoveArm::Response &res)
{
    CartesianPosition data;
    bool resres;
    int block=req.block;
    double vel=req.speed;
    int acc=req.acc;
    TrajectoryPoint trajectoryPoint;
    geometry_msgs::PoseStamped msg;
    int result;
    void * commandLayer_handle;
    //Function pointers to the functions we need
    //We load the library (Under Windows, use the function LoadLibrary)
    commandLayer_handle = dlopen("Kinova.API.USBCommandLayerUbuntu.so",RTLD_NOW|RTLD_GLOBAL);
    //We load the functions from the library (Under Windows, use GetProcAddress)
    MyInitAPI = (int (*)()) dlsym(commandLayer_handle,"InitAPI");
    MyCloseAPI = (int (*)()) dlsym(commandLayer_handle,"CloseAPI");
    MySetActuatorPID = (int (*)(unsigned int, float, float, float )) dlsym(commandLayer_handle,"SetActuatorPID");
    MySendAdvanceTrajectory = (int (*)(TrajectoryPoint)) dlsym(commandLayer_handle,"SendAdvanceTrajectory");
    MyStartControlAPI = (int (*)()) dlsym(commandLayer_handle,"StartControlAPI");
    MyGetCartesianPosition = (int (*)(CartesianPosition &)) dlsym(commandLayer_handle,"GetCartesianPosition");
    float rx, ry,rz;
    
    if((MyInitAPI == NULL) || (MyCloseAPI == NULL) || (MySendAdvanceTrajectory == NULL) || (MyStartControlAPI == NULL))
        {
                 std::cout << "Unable to initialize the command layer." <<  std::endl;
                return false;
        }

    result = (*MyInitAPI)();
    std::cout << "result of InitAPI() = " << result <<  std::endl <<  std::endl;
    //If the was loaded correctly
    //result = (*MyStartControlAPI)();
    trajectoryPoint=define_limitations(acc,vel,trajectoryPoint);

    trajectoryPoint.Position.Type = CARTESIAN_POSITION;
    //Since it is a cartesian position trajectory point those values will not be used but we initialize them anyway. :)
    trajectoryPoint.Position.Actuators.Actuator1 = 0.0f;
    trajectoryPoint.Position.Actuators.Actuator2 = 0.0f;
    trajectoryPoint.Position.Actuators.Actuator3 = 0.0f;
    trajectoryPoint.Position.Actuators.Actuator4 = 0.0f;
    trajectoryPoint.Position.Actuators.Actuator5 = 0.0f;
    trajectoryPoint.Position.Actuators.Actuator6 = 0.0f;
    //The delay value is only used if the position type is TIME_DELAY but we initialize it anyway.
    trajectoryPoint.Position.Delay = 0.0f;
    trajectoryPoint.Position.HandMode = POSITION_MODE;
    //We initialize the fingers.
    double distance=100;
    double dx = 0;
    double dy = 0;
    double dz = 0;
    ////////VERTICAL VISIBLE MOVEMENT
    if(req.block_owner=="vertical"){
    std::cout<<"vertical"<<std::endl;
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;    
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 0.04f;
    for(int i=0; i<1; i++){
    trajectoryPoint.Position.CartesianPosition.X = 0.2f;
    trajectoryPoint.Position.CartesianPosition.Y = 0.3f;
    trajectoryPoint.Position.CartesianPosition.Z = 1.1f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    trajectoryPoint.Position.CartesianPosition.Y = -0.3f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;}
    }

    ////////HORIZONTAL VISIBLE MOVEMENT
    else if(req.block_owner=="horizontal"){
    std::cout<<"horizontal"<<std::endl;
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;    
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 1.57f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    for(int i=0; i<1; i++){
    trajectoryPoint.Position.CartesianPosition.X = 0.6f;
    trajectoryPoint.Position.CartesianPosition.Y = -0.4f;
    trajectoryPoint.Position.CartesianPosition.Z = 0.4f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    trajectoryPoint.Position.CartesianPosition.Y = 0.4f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;}
    }

    ////////AVOID || BACK MOVEMENT
    else if(req.block_owner=="avoid" || req.block_owner=="back"){
    std::cout<<req.block_owner<<std::endl;
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;    
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.6f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 3.14f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    trajectoryPoint.Position.CartesianPosition.X = 0.1f;
    if(req.block_owner=="avoid"){trajectoryPoint.Position.CartesianPosition.Y = -0.2f;}
    else{trajectoryPoint.Position.CartesianPosition.Y = 0.2f;}
    trajectoryPoint.Position.CartesianPosition.Z = 0.3f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    }
    ////////NEAR || ATTENTION MOVEMENT || GRIPPER
    else if(req.block_owner=="attention"){
    std::cout<<req.block_owner<<std::endl;
    if (req.block_owner=="near"){
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f; }
    else{
    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);  
    }   
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 3.14f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    trajectoryPoint.Position.CartesianPosition.X = 0.1f;
    trajectoryPoint.Position.CartesianPosition.Y = -0.3f;
    trajectoryPoint.Position.CartesianPosition.Z = 0.4f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    }
    ////////NEAR || ATTENTION MOVEMENT || GRIPPER
    else if(req.block_owner=="near" || req.block_owner=="gripper"){
    std::cout<<req.block_owner<<std::endl;
    if (req.block_owner=="near"){
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f; }
    else{
    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);  
    }   
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 1.57f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    trajectoryPoint.Position.CartesianPosition.X = 0.5f;
    trajectoryPoint.Position.CartesianPosition.Y = -0.3f;
    trajectoryPoint.Position.CartesianPosition.Z = 0.4f; 
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    if (req.block_owner=="gripper"){
        for(int i=0;i<3;i++){
                               
                trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
                trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
                trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);

                (*MySendAdvanceTrajectory)(trajectoryPoint);

                trajectoryPoint.Position.Fingers.Finger1 = 30.0f;
                trajectoryPoint.Position.Fingers.Finger2 = 30.0f;
                trajectoryPoint.Position.Fingers.Finger3 = 30.0f;

        (*MySendAdvanceTrajectory)(trajectoryPoint);}
    }
    }
    else if(req.block_owner=="random"){
        rx = 0.2 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(0.4-0.2)));
        ry = -0.3 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(0.3-(-0.3))));
        rz = 0.2 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(0.8-0.2)));
        std::cout<<rx<<" "<<ry<<" "<<std::endl;
        trajectoryPoint.Position.CartesianPosition.X = rx;
        trajectoryPoint.Position.CartesianPosition.Y = ry;
        trajectoryPoint.Position.CartesianPosition.Y = rz;
        trajectoryPoint.Position.Fingers.Finger1 = 30.0f;
        trajectoryPoint.Position.Fingers.Finger2 = 30.0f;
        trajectoryPoint.Position.Fingers.Finger3 = 30.0f;
        (*MySendAdvanceTrajectory)(trajectoryPoint);
        while (distance>0.1){
                result = (*MyGetCartesianPosition)(data);
                dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
                dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
                dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
                distance=std::sqrt(dx*dx + dy*dy + dz*dz);
                msg.header.stamp=ros::Time::now();
                msg.pose.position.x=data.Coordinates.X;
                msg.pose.position.y=data.Coordinates.Y;
                msg.pose.position.z=data.Coordinates.Z;
                msg.pose.orientation.x=data.Coordinates.ThetaX;
                msg.pose.orientation.y=data.Coordinates.ThetaY;
                msg.pose.orientation.z=data.Coordinates.ThetaZ;
                pose_pub.publish(msg);
        }
        distance=100;

    }
    else if(req.block_owner=="front" || req.block_owner=="lateral" ){
    std::cout<<"horizontal"<<std::endl;
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 1.57f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    for(int i=0; i<1; i++){
    if (req.block_owner=="front"){
    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);
    trajectoryPoint.Position.CartesianPosition.X = 0.8f;
    trajectoryPoint.Position.CartesianPosition.Y = 0.0f;
    trajectoryPoint.Position.CartesianPosition.Z = 0.4f;}
    else{
    trajectoryPoint.Position.CartesianPosition.X = 0.5f;
    trajectoryPoint.Position.CartesianPosition.Y = -0.3f;
    trajectoryPoint.Position.CartesianPosition.Z = 0.4f; 
    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);  
    }
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    if (req.block_owner=="front"){trajectoryPoint.Position.CartesianPosition.X = 0.6f;
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;}
    else{
    trajectoryPoint.Position.CartesianPosition.X = 0.5f;
    trajectoryPoint.Position.CartesianPosition.Y = 0.3f;
    trajectoryPoint.Position.CartesianPosition.Z = 0.4f; 
    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);  
    }
    
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;}
    }

    else{
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 3.14f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    if (req.amplitude=="high"){
        trajectoryPoint.Position.CartesianPosition.Z = 0.4f;
    }
    else if (req.amplitude=="low"){
        trajectoryPoint.Position.CartesianPosition.Z = 0.25f;
    }
    else {
        trajectoryPoint.Position.CartesianPosition.Z = 0.3f;
    }

    if (req.traj=="no_fluent"){
        rx = 0.2 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(0.4-0.2)));
        ry = -0.2 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(0.2-(-0.2))));
        std::cout<<rx<<" "<<ry<<" "<<std::endl;
        trajectoryPoint.Position.CartesianPosition.X = rx;
        trajectoryPoint.Position.CartesianPosition.Y = ry;
        //trajectoryPoint.Position.CartesianPosition.ThetaX = -1.5 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(1.5-(-1.5))));
        //trajectoryPoint.Position.CartesianPosition.ThetaY = 1.5 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(4.6-1.5)));
        //trajectoryPoint.Position.CartesianPosition.ThetaZ = -1.5 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(1.5-(-1.5))));
        (*MySendAdvanceTrajectory)(trajectoryPoint);
        while (distance>0.1){
                result = (*MyGetCartesianPosition)(data);
                dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
                dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
                dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
                distance=std::sqrt(dx*dx + dy*dy + dz*dz);
                msg.header.stamp=ros::Time::now();
                msg.pose.position.x=data.Coordinates.X;
                msg.pose.position.y=data.Coordinates.Y;
                msg.pose.position.z=data.Coordinates.Z;
                msg.pose.orientation.x=data.Coordinates.ThetaX;
                msg.pose.orientation.y=data.Coordinates.ThetaY;
                msg.pose.orientation.z=data.Coordinates.ThetaZ;
                pose_pub.publish(msg);
        }
        distance=100;
    } 

    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 3.14f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
    if (req.block_owner=="robot" and block==0){
        trajectoryPoint.Position.CartesianPosition.X = 0.3f;
        trajectoryPoint.Position.CartesianPosition.Y = -0.3f;
    }
    else if (req.block_owner=="robot" and block==1){
        trajectoryPoint.Position.CartesianPosition.X = 0.3f;
        trajectoryPoint.Position.CartesianPosition.Y = -0.15f;
    }
    else if (req.block_owner=="robot" and block==2){
        trajectoryPoint.Position.CartesianPosition.X = 0.3f;
        trajectoryPoint.Position.CartesianPosition.Y = 0.0f;
    }
    else if (req.block_owner=="robot" and block==3){
        trajectoryPoint.Position.CartesianPosition.X = 0.3f;
        trajectoryPoint.Position.CartesianPosition.Y = 0.15f;
    }
    else if (req.block_owner=="robot" and block==4){
        trajectoryPoint.Position.CartesianPosition.X = 0.4f;
        trajectoryPoint.Position.CartesianPosition.Y = 0.15f;
    }
    else if (req.block_owner=="human" and block==0){
        trajectoryPoint.Position.CartesianPosition.X = 0.4f;
        trajectoryPoint.Position.CartesianPosition.Y = -0.15f;
    }
    else if (req.block_owner=="human" and block==1){
        trajectoryPoint.Position.CartesianPosition.X = 0.5f;
        trajectoryPoint.Position.CartesianPosition.Y = -0.1f;
    }
    else if (req.block_owner=="human" and block==2){
        trajectoryPoint.Position.CartesianPosition.X = 0.4f;
        trajectoryPoint.Position.CartesianPosition.Y = 0.0f;
    }
    else if (req.block_owner=="human" and block==3){
        trajectoryPoint.Position.CartesianPosition.X = 0.5f;
        trajectoryPoint.Position.CartesianPosition.Y = 0.1f;
    }
    else if (req.block_owner=="human" and block==4){
        trajectoryPoint.Position.CartesianPosition.X = 0.5f;
        trajectoryPoint.Position.CartesianPosition.Y = 0.2f;
    }
    else{
        ROS_INFO_STREAM("WRONG GOAL");
    }

    ROS_INFO_STREAM("GOING PREGRASP");

    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    
    ROS_INFO_STREAM("EXIT PREGRASP");
    if(req.style=="wrong"){
    trajectoryPoint.Position.CartesianPosition.Z = trajectoryPoint.Position.CartesianPosition.Z-0.05;
    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    
    trajectoryPoint.Position.CartesianPosition.Z = trajectoryPoint.Position.CartesianPosition.Z+0.05;  
    
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    }
    ROS_INFO_STREAM("GOING GRASP");
    trajectoryPoint.Position.CartesianPosition.Z = 0.08f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;  
    ROS_INFO_STREAM("EXIT GRASP"); 

    trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
    trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);

    (*MySendAdvanceTrajectory)(trajectoryPoint);
    

    ROS_INFO_STREAM("GOING PRERELEASE");
    if (req.amplitude=="high"){
        trajectoryPoint.Position.CartesianPosition.Z = 0.35f;
    }
    else if (req.amplitude=="low"){
        trajectoryPoint.Position.CartesianPosition.Z = 0.25f;
    }
    else {
        trajectoryPoint.Position.CartesianPosition.Z = 0.3f;
    }
    if (req.traj=="no_fluent"){
        rx = -0.1 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(0.4-(-0.1))));
        ry = -0.4 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/((-0.1)-(-0.4))));
        trajectoryPoint.Position.CartesianPosition.X = rx;
        trajectoryPoint.Position.CartesianPosition.Y = ry;
        //trajectoryPoint.Position.CartesianPosition.ThetaX = 0.0 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(3.14-0.0)));
        //trajectoryPoint.Position.CartesianPosition.ThetaY = 0.0 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(3.14-0.0)));
        //trajectoryPoint.Position.CartesianPosition.ThetaZ = 0.0 + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(3.14-0.0)));
        (*MySendAdvanceTrajectory)(trajectoryPoint);
        while (distance>0.1){
                result = (*MyGetCartesianPosition)(data);
                dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
                dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
                dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
                distance=std::sqrt(dx*dx + dy*dy + dz*dz);
                msg.header.stamp=ros::Time::now();
                msg.pose.position.x=data.Coordinates.X;
                msg.pose.position.y=data.Coordinates.Y;
                msg.pose.position.z=data.Coordinates.Z;
                msg.pose.orientation.x=data.Coordinates.ThetaX;
                msg.pose.orientation.y=data.Coordinates.ThetaY;
                msg.pose.orientation.z=data.Coordinates.ThetaZ;
                pose_pub.publish(msg);
        }
        distance=100;
    }
    
    trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
    trajectoryPoint.Position.CartesianPosition.ThetaY = 3.14f;
    trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;


    if(req.final_pose=="area1"){
        trajectoryPoint.Position.CartesianPosition.X=0.13;
        trajectoryPoint.Position.CartesianPosition.Y=-0.3;
    }
    else if (req.final_pose=="area2"){
        trajectoryPoint.Position.CartesianPosition.X=0.13;
        trajectoryPoint.Position.CartesianPosition.Y=-0.45;
    }
    else if (req.final_pose=="area3"){
        trajectoryPoint.Position.CartesianPosition.X=0.13;
        trajectoryPoint.Position.CartesianPosition.Y=-0.6;
    }
    else if (req.final_pose=="area4"){
        trajectoryPoint.Position.CartesianPosition.X=0.0;
        trajectoryPoint.Position.CartesianPosition.Y=-0.3;
    }
    else if (req.final_pose=="area5"){
        trajectoryPoint.Position.CartesianPosition.X=0.0;
        trajectoryPoint.Position.CartesianPosition.Y=-0.45;
    }
    else if (req.final_pose=="area6"){
        trajectoryPoint.Position.CartesianPosition.X=0.0;
        trajectoryPoint.Position.CartesianPosition.Y=-0.6;
    }
    else if (req.final_pose=="area7"){
        trajectoryPoint.Position.CartesianPosition.X=-0.15;
        trajectoryPoint.Position.CartesianPosition.Y=-0.3;
    }
    else if (req.final_pose=="area8"){
        trajectoryPoint.Position.CartesianPosition.X=-0.15;
        trajectoryPoint.Position.CartesianPosition.Y=-0.45;
    }
    else if (req.final_pose=="area9"){
        trajectoryPoint.Position.CartesianPosition.X=-0.15;
        trajectoryPoint.Position.CartesianPosition.Y=-0.6;
    }
    
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    ROS_INFO_STREAM("EXIT PRERELEASE");
    ROS_INFO_STREAM("GOING RELEASE");
    
    if(req.style=="wrong"){
        trajectoryPoint.Position.CartesianPosition.X=0.2f;
    }
    trajectoryPoint.Position.CartesianPosition.Z=0.04f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;
    ROS_INFO_STREAM("EXIT RELEASE");

    ROS_INFO_STREAM("OPEN HAND");
    
    trajectoryPoint.Position.Fingers.Finger1 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger2 = 6.0f;
    trajectoryPoint.Position.Fingers.Finger3 = 6.0f;
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    trajectoryPoint.Position.CartesianPosition.X=0.2;
    trajectoryPoint.Position.CartesianPosition.Y=-0.2;
    if (req.amplitude=="high"){
        trajectoryPoint.Position.CartesianPosition.Z = 0.35f;
    }
    else if (req.amplitude=="low"){
        trajectoryPoint.Position.CartesianPosition.Z = 0.25f;
    }
    else {
        trajectoryPoint.Position.CartesianPosition.Z = 0.3f;
    }
    (*MySendAdvanceTrajectory)(trajectoryPoint);
    while (distance>0.1){
            result = (*MyGetCartesianPosition)(data);
            dx=data.Coordinates.X-trajectoryPoint.Position.CartesianPosition.X;
            dy=data.Coordinates.Y-trajectoryPoint.Position.CartesianPosition.Y;
            dz=data.Coordinates.Z-trajectoryPoint.Position.CartesianPosition.Z;
            distance=std::sqrt(dx*dx + dy*dy + dz*dz);
            msg.header.stamp=ros::Time::now();
            msg.pose.position.x=data.Coordinates.X;
            msg.pose.position.y=data.Coordinates.Y;
            msg.pose.position.z=data.Coordinates.Z;
            msg.pose.orientation.x=data.Coordinates.ThetaX;
            msg.pose.orientation.y=data.Coordinates.ThetaY;
            msg.pose.orientation.z=data.Coordinates.ThetaZ;
            pose_pub.publish(msg);
    }
    distance=100;

   } 
  return true;
}




int main(int argc, char **argv)
{
       ros::init(argc, argv, "kinova_move_server");
       ros::NodeHandle n;
       pose_pub = n.advertise<geometry_msgs::PoseStamped>("kinova_pose", 1000);
        
        ros::Subscriber sub;
        ros::AsyncSpinner spinner(2);
        spinner.start();  

        
        ros::ServiceServer service = n.advertiseService("/kinova_server", kinova_motion_srv);
       
        
     
       
        while (true){
            sleep(1);
        }
        return 0; 
}
