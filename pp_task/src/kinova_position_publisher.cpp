#include "ros/ros.h"
#include <iostream>
#include <dlfcn.h> //Ubuntu
#include <KinovaTypes.h>
#include <Kinova.API.CommLayerUbuntu.h>
#include "geometry_msgs/PoseStamped.h"
//Note that under windows, you may/will have to perform other #include
using namespace std;
int main(int argc, char **argv)
{
        int result;
        CartesianPosition data;
        cout << "GetCartesianPosition function example" << endl;
        //Handle for the library's command layer.
        void * commandLayer_handle;
        //Function pointers to the functions we need
        int (*MyInitAPI)();
        int (*MyCloseAPI)();
        int (*MyGetCartesianPosition)(CartesianPosition &);
        //We load the library (Under Windows, use the function LoadLibrary)
        commandLayer_handle = dlopen("Kinova.API.USBCommandLayerUbuntu.so",RTLD_NOW|RTLD_GLOBAL);
        //We load the functions from the library (Under Windows, use GetProcAddress)
        MyInitAPI = (int (*)()) dlsym(commandLayer_handle,"InitAPI");
        MyCloseAPI = (int (*)()) dlsym(commandLayer_handle,"CloseAPI");
        MyGetCartesianPosition = (int (*)(CartesianPosition &)) dlsym(commandLayer_handle,"GetCartesianPosition");
        //If the was loaded correctly
        if((MyInitAPI == NULL) || (MyCloseAPI == NULL) || (MyGetCartesianPosition == NULL))
        {
                cout << "Unable to initialize the command layer." << endl;
        }
        else
        {
                ros::init(argc, argv, "kinova_publisher");
                ros::NodeHandle n;

                ros::Publisher pose_pub = n.advertise<geometry_msgs::PoseStamped>("kinova_pose", 1000);

                ros::Rate loop_rate(10);
                cout << "The command has been initialized correctly." << endl << endl;
                cout << "Calling the method InitAPI()" << endl;
                result = (*MyInitAPI)();
                cout << "result of InitAPI() = " << result << endl;
                geometry_msgs::PoseStamped msg;
                while(true){
                result = (*MyGetCartesianPosition)(data);
                msg.header.stamp=ros::Time::now();
                msg.pose.position.x=data.Coordinates.X;
                msg.pose.position.y=data.Coordinates.Y;
                msg.pose.position.z=data.Coordinates.Z;
                msg.pose.orientation.x=data.Coordinates.ThetaX;
                msg.pose.orientation.y=data.Coordinates.ThetaY;
                msg.pose.orientation.z=data.Coordinates.ThetaZ;
                pose_pub.publish(msg);
                cout << "       Position X : " << data.Coordinates.X << endl;
                cout << "       Position Y : " << data.Coordinates.Y << endl;
                cout << "       Position Z : " << data.Coordinates.Z << endl;
                cout << "  Position ThetaX : " << data.Coordinates.ThetaX << endl;
                cout << "  Position ThetaY : " << data.Coordinates.ThetaY << endl;
                cout << "  Position ThetaZ : " << data.Coordinates.ThetaZ << endl;
                pose_pub.publish(msg);
                }
                result = (*MyCloseAPI)();
                cout << "result of CloseAPI() = " << result << endl;
        }
        return 0;
}