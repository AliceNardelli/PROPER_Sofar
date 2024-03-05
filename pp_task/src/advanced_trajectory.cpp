#include <iostream>
#include <dlfcn.h> //Ubuntu
#include <KinovaTypes.h>
#include <Kinova.API.CommLayerUbuntu.h>
//Note that under windows, you may/will have to perform other #include
using namespace std;
int main()
{
        int result;
        cout << "SendAdvanceTrajectory function example" << endl;
        //Handle for the library's command layer.
        void * commandLayer_handle;
        //Function pointers to the functions we need
        int (*MyInitAPI)();
        int (*MyCloseAPI)();
        int (*MySendAdvanceTrajectory)(TrajectoryPoint command);
        int (*MyStartControlAPI)();
        //We load the library (Under Windows, use the function LoadLibrary)
        commandLayer_handle = dlopen("Kinova.API.USBCommandLayerUbuntu.so",RTLD_NOW|RTLD_GLOBAL);
        //We load the functions from the library (Under Windows, use GetProcAddress)
        MyInitAPI = (int (*)()) dlsym(commandLayer_handle,"InitAPI");
        MyCloseAPI = (int (*)()) dlsym(commandLayer_handle,"CloseAPI");
        MySendAdvanceTrajectory = (int (*)(TrajectoryPoint)) dlsym(commandLayer_handle,"SendAdvanceTrajectory");
        MyStartControlAPI = (int (*)()) dlsym(commandLayer_handle,"StartControlAPI");
        //If the was loaded correctly
        if((MyInitAPI == NULL) || (MyCloseAPI == NULL) || (MySendAdvanceTrajectory == NULL) || (MyStartControlAPI == NULL))
        {
                cout << "Unable to initialize the command layer." << endl;
        }
        else
        {
                cout << "The command has been initialized correctly." << endl << endl;
                cout << "Calling the method InitAPI()" << endl;
                result = (*MyInitAPI)();
                cout << "result of InitAPI() = " << result << endl << endl;
                //We prepare the virtual joystick command that will be sent to the robotic arm.
                TrajectoryPoint trajectoryPoint;
                //Initializing the point.
                trajectoryPoint.Limitations.accelerationParameter1 = 0.0f; //Not implemented yet but will be in a future release.
                trajectoryPoint.Limitations.accelerationParameter2 = 0.0f; //Not implemented yet but will be in a future release.
                trajectoryPoint.Limitations.accelerationParameter3 = 0.0f; //Not implemented yet but will be in a future release.
                trajectoryPoint.Limitations.forceParameter1 = 0.0f; //Not implemented yet but will be in a future release.
                trajectoryPoint.Limitations.forceParameter2 = 0.0f; //Not implemented yet but will be in a future release.
                trajectoryPoint.Limitations.forceParameter3 = 0.0f; //Not implemented yet but will be in a future release.
                trajectoryPoint.Limitations.speedParameter1 = 0.08f;//We limit the translation velocity to 8 cm per second.
                trajectoryPoint.Limitations.speedParameter2 = 0.6f; //We limit the orientation velocity to 0.6 RAD per second
                trajectoryPoint.Limitations.speedParameter3 = 0.08f;
                trajectoryPoint.LimitationsActive = 1;
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

                
                trajectoryPoint.Position.CartesianPosition.X = 0.4f;
                trajectoryPoint.Position.CartesianPosition.Y = -0.4f;
                trajectoryPoint.Position.CartesianPosition.Z = 0.4f;
                //We set the orientation part of the position (unit is RAD)
                trajectoryPoint.Position.CartesianPosition.ThetaX = 0.04f;
                trajectoryPoint.Position.CartesianPosition.ThetaY = 1.57f;
                trajectoryPoint.Position.CartesianPosition.ThetaZ = 1.57f;
                (*MySendAdvanceTrajectory)(trajectoryPoint); 
/*
                for(int i=0;i<3;i++){
                               
                trajectoryPoint.Position.Fingers.Finger1 = float(0.8*6800.0);
                trajectoryPoint.Position.Fingers.Finger2 = float(0.8*6800.0);
                trajectoryPoint.Position.Fingers.Finger3 = float(0.8*6800.0);

                (*MySendAdvanceTrajectory)(trajectoryPoint);

                trajectoryPoint.Position.Fingers.Finger1 = 30.0f;
                trajectoryPoint.Position.Fingers.Finger2 = 30.0f;
                trajectoryPoint.Position.Fingers.Finger3 = 30.0f;

                (*MySendAdvanceTrajectory)(trajectoryPoint);}*/
                cout << endl << "Calling the method CloseAPI()" << endl;
                result = (*MyCloseAPI)();
                cout << "result of CloseAPI() = " << result << endl;
        }
        return 0;
}