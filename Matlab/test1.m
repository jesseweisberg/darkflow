%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
% Purpose: Draw bounding box and class label about detected object 
% 
% Author:  Jesse Weisberg, 6/13/17
%~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

close all;
clear all; 

fig = figure;
% fig.Position =[0 0 1280 720];
cam=webcam;

while (1)    
    [class, boundingBox] = objData('classFile.txt');
%     class
%     boundingBox
    frame = snapshot(cam);
    frame = insertShape(frame,'rectangle',boundingBox,'LineWidth',5);
    frame = insertText(frame, boundingBox(1:2), class);
    imshow(frame);  
end