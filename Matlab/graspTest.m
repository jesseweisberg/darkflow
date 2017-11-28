%% grip with QR
a=arduino();
cam=webcam; % connect the camera
figure();
pos = .5; %potentiometer reading which corresponds to position fingers should close on
temp=[];

% thresholds ? [thumb pinky ring middle index]
% mins = [.0440 .098 .8162 1.602 0.1271]
% maxes = [
% threshold inverse relationship with amount finger contracts
% threshGlass = [.5 .5 .5 .5 .5]; %standard contraction 
threshGlass = [2 2 .8 1.5 1]; %standard contraction 
threshPen = [.0538 .1075 .0489 1.5689 .9335];
threshBrush = [4.9 .2 .2 .5 .2];
threshCap = [.05 4.5 4.5 4.5 1.3392];
while (1)    
    % position feedback
    P0=readVoltage(a,'A0');
    P1=readVoltage(a,'A1');
    P2=readVoltage(a,'A2');
    P3=readVoltage(a,'A3');
    P4=readVoltage(a,'A4');
    temp=[temp [P0;P1;P2;P3;P4]];
    subplot(2,1,1);
    plot(temp');
    title('Finger Positions');
%     
    picture=snapshot(cam); % take a picture
%     picture=imresize(picture,[227,227]); % resize
    subplot(2,1,2);
    imshow(picture);
    title('Detecting Object');
    data = readClasses('classFile.txt'); % decode QR_code
    
    class = data(1); 
    tlx = data(2); tly = data(3); blx = data(4); bly = data(5);
    
    if strcmp(class,'apple')
        % insert EMG thresholding or proportional control
        %%EMG thresholding        
%         v = readVoltage(a,'A6')         
%         if v>2
%             label='aa';
%             writePosition(data(2_, 0);
%             pause(2);
%             break;
%         end
        
        %run the grip until fingers reach desired locations
        picture=snapshot(cam);
        subplot(2,1,2);
        title('Apple Detected');
             imshow(picture);

         temp=contract(a, threshGlass, temp);
         disp('Apple');
    end
   
    if strcmp(class, 'pen')
        picture=snapshot(cam);
        subplot(2,1,2);
         title('Pen Detected');
             imshow(picture);

         temp=contract(a, threshPen, temp);
         data
    end
    if strcmp(class, 'brush')
        picture=snapshot(cam);
        subplot(2,1,2);
         title('Brush Detected')
             imshow(picture);

         temp=contract(a, threshBrush, temp);
         data
    end  
    
    if strcmp(class, 'cap')
        picture=snapshot(cam);
        subplot(2,1,2);
         title('Cap Detected');
             imshow(picture);

         temp=contract(a, threshCap, temp);
         data
    end
     
    openAll(a);
end
