%% Live Webcam Classification
% Use deep learning model to classify handwritten numbers live with a webcam
%
% Copyright 2017 The MathWorks, Inc.

% Load model
clear
load MNISTModel.mat

% Get images from the webcam and classify using the model
camera = webcam;

while true
    
    imOriginal = camera.snapshot;
    
    imFinal = preprocessImage(imOriginal);
    label = classify(net,imFinal);
    
    image(imOriginal);
    title(char(label));
    drawnow; 
    
end