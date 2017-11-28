function vPlot=contract(a,thresh, vPlot)
    temp=1;
    while (temp==1)
        P0=readVoltage(a,'A0');
        P1=readVoltage(a,'A1');
        P2=readVoltage(a,'A2');
        P3=readVoltage(a,'A3');
        P4=readVoltage(a,'A4');
        
        vPlot = [vPlot [P0;P1;P2;P3;P4]];
%         subplot(2,1,1);
%         plot(vPlot');
        
        if(P0>thresh(1))
            writeDigitalPin(a,'D13',0); % contract 1
            writeDigitalPin(a,'D12',1);
        else
            writeDigitalPin(a,'D13',0); % stop 1
            writeDigitalPin(a,'D12',0);
        end
        if(P1>thresh(2))
            writeDigitalPin(a,'D11',0); % contract 2
            writeDigitalPin(a,'D10',1);
        else
            writeDigitalPin(a,'D11',0); % stop 2
            writeDigitalPin(a,'D10',0);
        end
        if(P2>thresh(3))
            writeDigitalPin(a,'D09',0); % contract 3
            writeDigitalPin(a,'D08',1);
        else
            writeDigitalPin(a,'D09',0); % stop 3
            writeDigitalPin(a,'D08',0);
        end
        if(P3>thresh(4))
            writeDigitalPin(a,'D07',0); % contract 4
            writeDigitalPin(a,'D06',1);
        else
            writeDigitalPin(a,'D07',0); % stop 4
            writeDigitalPin(a,'D06',0);
        end
        if(P4>thresh(5))
            writeDigitalPin(a,'D05',0); % contract 5
            writeDigitalPin(a,'D04',1);
        else
            writeDigitalPin(a,'D05',0); % stop 5
            writeDigitalPin(a,'D04',0);
        end
        if((P0<thresh(1))&&(P1<thresh(2))&&(P2<thresh(3))&&(P3<thresh(4))&&(P4<thresh(5)))
            temp=0;
            pause(1);
        end
    end
end

    