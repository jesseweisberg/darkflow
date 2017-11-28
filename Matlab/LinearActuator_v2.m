%% init arduino
a = arduino();

%% initialization - extended position no 5 - Thumb
clear v0
clear v1
clear time

% starting conditions - extended positions
writeDigitalPin(a,'D13',1); % for actuator 1 (thumb)
writeDigitalPin(a,'D12',0);
writeDigitalPin(a,'D11',1); % for actuator 2 (pinky)
writeDigitalPin(a,'D10',0);
writeDigitalPin(a,'D9',1); % for actuator 3 (ring)
writeDigitalPin(a,'D8',0);
writeDigitalPin(a,'D7',1); % for actuator 4 (middle)
writeDigitalPin(a,'D6',0);
writeDigitalPin(a,'D5',1); % for actuator 5 (index)
writeDigitalPin(a,'D4',0);

%% open and close continuously fo 10 sec
tic;
i=0;
while toc<100
    P0=readVoltage(a,'A0');
    P1=readVoltage(a,'A1');
    P2=readVoltage(a,'A2');
    P3=readVoltage(a,'A3');
    P4=readVoltage(a,'A4');

    if P0<0.5
        writeDigitalPin(a,'D13',1); % extend 1
        writeDigitalPin(a,'D12',0);
    end
    if P0>4.5
        writeDigitalPin(a,'D13',0); % contract 1
        writeDigitalPin(a,'D12',1);
    end
    if P1<0.5
        writeDigitalPin(a,'D11',1); % extend 2
        writeDigitalPin(a,'D10',0);
    end
    if P1>4.5
        writeDigitalPin(a,'D11',0); % contract 2
        writeDigitalPin(a,'D10',1);
    end
    if P2<0.5
        writeDigitalPin(a,'D9',1); % extend 3
        writeDigitalPin(a,'D8',0);
    end
    if P2>4.5
        writeDigitalPin(a,'D9',0); % contract 3
        writeDigitalPin(a,'D8',1);
    end
    if P3<0.5
        writeDigitalPin(a,'D7',1); % extend 4
        writeDigitalPin(a,'D6',0);
    end
    if P3>4.5
        writeDigitalPin(a,'D7',0); % contract 4
        writeDigitalPin(a,'D6',1);
    end
    if P4<0.5
        writeDigitalPin(a,'D5',1); % extend 5
        writeDigitalPin(a,'D4',0);
    end
    if P4>4.5
        writeDigitalPin(a,'D5',0); % contract 5
        writeDigitalPin(a,'D4',1);
    end
    
    i=i+1;
    time(i)=toc;
    v0(i)=P0;
    v1(i)=P1;
    v2(i)=P2;
    v3(i)=P3;
    v4(i)=P4;
    plot(time,v0,'b');hold on;
    plot(time,v1,'r');hold on;
    plot(time,v2,'g');hold on;
    plot(time,v3,'k');hold on;
    plot(time,v4,'y');
    drawnow;
end

%% open
writeDigitalPin(a,'D13',1); % extend 1
writeDigitalPin(a,'D12',0);

writeDigitalPin(a,'D11',1); % extend 2
writeDigitalPin(a,'D10',0);

writeDigitalPin(a,'D09',1); % extend 3
writeDigitalPin(a,'D08',0);

writeDigitalPin(a,'D07',1); % extend 4
writeDigitalPin(a,'D06',0);

writeDigitalPin(a,'D05',1); % extend 5
writeDigitalPin(a,'D04',0);

%% close
writeDigitalPin(a,'D13',0); % contract 1
writeDigitalPin(a,'D12',1);

writeDigitalPin(a,'D11',0); % contract 2
writeDigitalPin(a,'D10',1);

writeDigitalPin(a,'D09',0); % contract 3
writeDigitalPin(a,'D08',1);

writeDigitalPin(a,'D07',0); % contract 4
writeDigitalPin(a,'D06',1);

writeDigitalPin(a,'D05',0); % contract 5
writeDigitalPin(a,'D04',1);

%% stop everything
writeDigitalPin(a,'D13',0); % stop 1
writeDigitalPin(a,'D12',0);

writeDigitalPin(a,'D11',0); % stop 2
writeDigitalPin(a,'D10',0);

writeDigitalPin(a,'D09',0); % stop 3
writeDigitalPin(a,'D08',0);

writeDigitalPin(a,'D07',0); % stop 4
writeDigitalPin(a,'D06',0);

writeDigitalPin(a,'D05',0); % stop 5
writeDigitalPin(a,'D04',0);

%% two finger pinch - close no 1 and no 5
while (1)
    P3=readVoltage(a,'A3');
    P4=readVoltage(a,'A4');
    
    writeDigitalPin(a,'D13',0); % contract 1
    writeDigitalPin(a,'D12',1);
        
    writeDigitalPin(a,'D5',0); % contract 5
    writeDigitalPin(a,'D4',1);
    
    if (P3<0.5) && (P4<0.5)
        writeDigitalPin(a,'D13',0); % stop 4
        writeDigitalPin(a,'D12',0);
        writeDigitalPin(a,'D5',0); % stop 5
        writeDigitalPin(a,'D4',0);
        break;
    end
end

%% 4 finger grab
while (1)
    P0=readVoltage(a,'A0');
    P1=readVoltage(a,'A1');
    P2=readVoltage(a,'A2');
    P3=readVoltage(a,'A3');
    
    writeDigitalPin(a,'D13',0); % contract 1
    writeDigitalPin(a,'D12',1);
    writeDigitalPin(a,'D11',0); % contract 2
    writeDigitalPin(a,'D10',1);
    writeDigitalPin(a,'D9',0); % contract 3
    writeDigitalPin(a,'D8',1);
    writeDigitalPin(a,'D7',0); % contract 4
    writeDigitalPin(a,'D6',1);
    
    if (P0<0.5) && (P1<0.5) && (P2<0.5) && (P3<0.5)
        writeDigitalPin(a,'D13',0); % stop 1
        writeDigitalPin(a,'D12',0);
        writeDigitalPin(a,'D11',0); % stop 2
        writeDigitalPin(a,'D10',0);
        writeDigitalPin(a,'D9',0); % stop 3
        writeDigitalPin(a,'D8',0);
        writeDigitalPin(a,'D7',0); % stop 4
        writeDigitalPin(a,'D6',0);
        break;
    end
end

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
    data = decode_qr(flip(picture,2)); % decode QR_code
    
    if strcmp(data,'glass')
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
        title('Water Bottle Detected');
             imshow(picture);

         temp=contract(a, threshGlass, temp);
         disp('Water Bottle');
    end
   
    if strcmp(data, 'pen')
        picture=snapshot(cam);
        subplot(2,1,2);
         title('Pen Detected');
             imshow(picture);

         temp=contract(a, threshPen, temp);
         data
    end
    if strcmp(data, 'brush')
        picture=snapshot(cam);
        subplot(2,1,2);
         title('Brush Detected')
             imshow(picture);

         temp=contract(a, threshBrush, temp);
         data
    end  
    
    if strcmp(data, 'cap')
        picture=snapshot(cam);
        subplot(2,1,2);
         title('Cap Detected');
             imshow(picture);

         temp=contract(a, threshCap, temp);
         data
    end
     
    openAll(a);
end
