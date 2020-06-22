% Helper script to convert all audio files into spectrograms

% Training neural networks is easiest when the inputs to the network 
% have a reasonably smooth distribution and are normalized. 

% To obtain data with a smoother distribution, take the logarithm of the 
% spectrograms using a small offset. We include this offset so that we do 
% not inadvertantly calculate the log of 0. 

% You can think of this calculation as being similar to converting audio 
% amplitude into decibels.

addpath(fullfile(matlabroot,'examples','audio','main'))
epsil = 1e-6;


if processLive
    reset(adsTrain)
    XTrain = speechSpectrograms(adsTrain,segmentDuration,frameDuration,hopDuration,numBands);
    XTrain = log10(XTrain + epsil);
    
    reset(adsValidation)
    XValidation = speechSpectrograms(adsValidation,segmentDuration,frameDuration,hopDuration,numBands);
    XValidation = log10(XValidation + epsil);
    
    reset(adsTest)
    XTest = speechSpectrograms(adsTest,segmentDuration,frameDuration,hopDuration,numBands);
    XTest = log10(XTest + epsil);
else
    dataLocation = fullfile([filesep,'MATLAB Drive', filesep, 'Workshop', filesep, 'LargeFiles', filesep, '08-SpeechSpectrograms', filesep, 'speechspectrograms.mat']);
    load(dataLocation)
end

YTrain = adsTrain.Labels;
YValidation = adsValidation.Labels;
YTest = adsTest.Labels;