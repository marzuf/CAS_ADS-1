classdef weightedClassificationLayer < nnet.layer.ClassificationLayer
        
    properties
        % (Optional) Layer properties.

        % Layer properties go here.
        ClassWeights
    end
 
    methods
        function layer = weightedClassificationLayer(classWeights, name)           
            % layer = weightedClassificationLayer(classWeights) creates a
            % weighted cross entropy loss layer. classWeights is a row
            % vector of weights corresponding to the classes in the order
            % that they appear in the training data.
            % 
            % layer = weightedClassificationLayer(classWeights, name)
            % additionally specifies the layer name.
            
            layer.ClassWeights = classWeights;
            
            if nargin == 2
                layer.Name = name;
            end
            
            layer.Description = 'Weighted cross entropy';
        end

        function loss = forwardLoss(layer, Y, T)
            % Return the loss between the predictions Y and the 
            % training targets T.
            %
            % Inputs:
            %         layer - Output layer
            %         Y     – Predictions made by network
            %         T     – Training targets
            %
            % Output:
            %         loss  - Loss between Y and T
            N = size(Y,4);
            Y = squeeze(Y);
            T = squeeze(T);
            W = layer.ClassWeights;

            % Layer forward loss function goes here.
            loss = -sum(W*(T.*log(Y)))/N;
        end
        
        function dLdY = backwardLoss(layer, Y, T)
            % Backward propagate the derivative of the loss function.
            %
            % Inputs:
            %         layer - Output layer
            %         Y     – Predictions made by network
            %         T     – Training targets
            %
            % Output:
            %         dLdY  - Derivative of the loss with respect to the predictions Y
            [~,~,K,N] = size(Y);
            Y = squeeze(Y);
            T = squeeze(T);
            W = layer.ClassWeights;
			
            dLdY = -(W'.*T./Y)/N;
            dLdY = reshape(dLdY,[1 1 K N]);
            % Layer backward loss function goes here.
        end
    end
end