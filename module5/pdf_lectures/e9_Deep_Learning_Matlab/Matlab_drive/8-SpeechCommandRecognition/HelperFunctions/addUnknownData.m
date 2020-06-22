isUnknown = ~ismember(ads.Labels,categorical([commands,"_background_noise_"]));

probIncludeUnknown = 0.1;
mask = rand(numel(ads.Labels),1) < probIncludeUnknown;
isUnknown = isUnknown & mask;
ads.Labels(isUnknown) = categorical("unknown");