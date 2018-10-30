# Drone-Stabilization and Localization indoors

## About
* This project aims at stabilizing drones indoor, and maintaining its equilibrium around a certain point using error correction mechanism.
* PID mechanism has been used for stabilization.
* The branch of mathematics that deal with this is called control theory.

## Implementation

* A yellow colored table tennis ball is pinned on drone, this ball is detected using external cameras.
* The ball is detected using HSV color space object detection. Here we get the bounding box of the contour of ball.
* The x,y co-ordinates of this ball give the location of drone in 2D dimensional space.
* The 3rd dimension movements can be controlled using another external camera, but this is beyond the scope of this project.
* The x,y co-ordinates are adjusted in relation to P,I and D values and the error.
* The error is calculated as the distance b/w center of the frame and the center of the ball(x,y).
* The estimated correction is added to the original values of throttle and roll and given as input to drone.
* The estimated value of roll and throttle is then sent to raspberry pi, that is controlling the drone.
* The drone can be moved in space by changing the reference point from center of frame to any other point in frame.
* This results in stabilization of drone around the other point.

## Usage

* The main_stabilize file sends values of throttle and roll to raspberry pi. For this just create a hotspot from your computer, and connect
raspberry pi to it wirelessly.
* Receive those commands on raspberry pi and write them to drone via serial or any other way.
