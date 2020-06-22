############################################################################################################################# DEFINED IN THIS SCRIPT (my_cnn_functions.py):
# def get_minibatch_xy(index_list, i_batch, n_to_sample, full_inputDF , y_obs_colnbr, seq_len):
# def crop_seq(seq, mp_step, check_size):
# def get_conv1d_layer(conv_input,nbr_filters, size_kernel, step_stride, type_padding,activ_function):
# def get_mp1d_layer(mp_input,  size_mp,step_stride, type_padding):
# def conv1d_model_CN_MP(CN_input, CN_nbr_filters, CN_size_kernel, CN_step_stride, CN_type_padding, CN_activ_function, MP_mp_size, MP_step_stride, MP_type_padding, minibatch_size, bin_seq_len, n_chip):
# def loss_plot(train_data, valid_data, image_file=None):
# def print_in_file(mytext, filename):

#############################################################################################################################
############################################################################################################################# get_minibatch_xy
#############################################################################################################################


def get_minibatch_xy(index_list, i_batch, n_to_sample, full_inputDF , y_obs_colnbr, seq_len):
  # - index_list = the list with the indices to subset (start position of the sequence)
  # - i_batch = current batch iteration
  # - n_to_sample = the number of samples to subset
  # - full_inputDF = the dataframe from which I will subset the sample data
  # - y_obs_colnbr = column number that stores the boundary score
  # - seq_len = the length of the sequence 
  
  # - return: the x_input and the y_obs for the current minibatch
  
  # retrieve the samples for current minibatch
  # the index list stores all start positions
  y_obs_colname = full_inputDF.columns[y_obs_colnbr]
  
  chip_nbr = full_inputDF.shape[1]-1
  
  # -> subset all start positions (0 based, end position not included)
  mini_batch_start_idx = i_batch * n_to_sample   # if n_to_sample=5, i_batch=0 -> 0, i_batch=1 -> 5, i_batch=2 -> 10
  mini_batch_end_idx = (i_batch+1) * n_to_sample # if n_to_sample=5, i_batch=0 -> 5, i_batch=1 -> 5, i_batch=2 -> 10
  
  assert mini_batch_start_idx >= 0
  assert mini_batch_end_idx <= len(index_list)

  mini_batch_start_positions = index_list[mini_batch_start_idx:mini_batch_end_idx]
  mini_batch_idx_seq = []
  _ = [mini_batch_idx_seq.extend(range(x, (x+seq_len))) for x in mini_batch_start_positions ]

  assert (len(mini_batch_start_positions)) * seq_len == len(mini_batch_idx_seq)
  assert max(mini_batch_idx_seq) <= full_inputDF.shape[0]
  assert min(mini_batch_idx_seq) >= 0
  assert len(mini_batch_idx_seq) == n_to_sample * seq_len
  
  # select the x_input => the chip values
  x_input = full_inputDF.iloc[mini_batch_idx_seq, :].drop(y_obs_colname, axis=1)
  x_input.reset_index(drop=True, inplace=True)

  # select the y_input => the observed sequence of bin scores
  y_input = full_inputDF.iloc[mini_batch_idx_seq, [y_obs_colnbr]] # this returns a DataFrame
  y_input.reset_index(drop=True, inplace=True)


  assert x_input.shape == (n_to_sample * seq_len, chip_nbr)
  assert y_input.shape == ((n_to_sample * seq_len), 1)
  
  
  np_x_input = x_input.values # to_numpy() in later pandas version !
  x_input_reshaped = np_x_input.reshape(n_to_sample, seq_len, chip_nbr)
  assert all(x_input_reshaped[0,0,:] == x_input.iloc[0,:])

  np_y_input = y_input.values 
  y_input_reshaped = np_y_input.reshape(n_to_sample, seq_len, 1)
  assert all(y_input_reshaped[0,0,:] == y_input.iloc[0,:])

  return x_input_reshaped, y_input_reshaped


#############################################################################################################################
############################################################################################################################# crop_seq
#############################################################################################################################


def crop_seq(seq, mp_step, check_size):
  tmp = seq.reshape(-1)
  seq_cropped = tmp[::mp_step] ## if "valid": delta:-delta:crop_step
  assert len(seq_cropped.reshape(-1)) == check_size
  return seq_cropped

#############################################################################################################################
############################################################################################################################# get_conv1d_layer
#############################################################################################################################

def get_conv1d_layer(conv_input,
                    nbr_filters,
                    size_kernel,
                    step_stride,
                    type_padding,
                    activ_function):

  import tensorflow as tf

  my_layer = tf.layers.conv1d(inputs = conv_input, 
                            filters=nbr_filters, 
                            kernel_size=size_kernel, 
                            strides = step_stride, 
                            padding = type_padding,
                            activation = activ_function)  



  return my_layer

#############################################################################################################################
############################################################################################################################# get_mp1d_layer
#############################################################################################################################

def get_mp1d_layer(mp_input, 
                  size_mp,
                  step_stride,
                  type_padding):
  import tensorflow as tf

  return tf.layers.max_pooling1d(inputs = mp_input, 
                                     pool_size=size_mp, 
                                     strides=step_stride, 
                                     padding = type_padding)

#############################################################################################################################
############################################################################################################################# conv1d_model_CN_MP
#############################################################################################################################

def conv1d_model_CN_MP(CN_input,
                   CN_nbr_filters,
                   CN_size_kernel,
                   CN_step_stride,
                   CN_type_padding,
                   CN_activ_function,
                   MP_mp_size,
                   MP_step_stride,
                   MP_type_padding, 
                   minibatch_size, 
                   bin_seq_len, 
                   n_chip):
  import tensorflow as tf

  from myutils_v2 import get_output_shape_convLayer
  from myutils_v2 import get_output_shape_poolLayer


  ### CALL THE NN TO RETRIEVE THE PREDICTIONS
  out_CN1 =  get_conv1d_layer(conv_input=CN_input,
                    nbr_filters=CN_nbr_filters,
                    size_kernel=CN_size_kernel,
                    step_stride=CN_step_stride,
                    type_padding=CN_type_padding,
                    activ_function=CN_activ_function)
  
  in_MP1 = out_CN1
  
  outCN1_size = get_output_shape_convLayer(
                    input_shape = [1,bin_seq_len,n_chip],
                    kernel_size = CN_size_kernel,
                    n_kernel = CN_nbr_filters,
                    padding_type = CN_type_padding.lower(),
                    stride_size = CN_step_stride)

  out_MP1 = get_mp1d_layer(mp_input = in_MP1,
                  size_mp = MP_mp_size,
                  step_stride = MP_step_stride,
                  type_padding = MP_type_padding
  ) 

  outMP1_size = get_output_shape_poolLayer(input_shape = outCN1_size,
                   pool_size = MP_mp_size,
                   stride_size = MP_step_stride)
      
  foo = tf.reshape(out_CN1, tuple([minibatch_size,bin_seq_len, CN_nbr_filters]))
  
  foo = tf.reshape(out_MP1, tuple([minibatch_size,bin_seq_len//MP_mp_size, CN_nbr_filters]))
    
  # final CN layer to get the predicted values
  out_CNfinal =  get_conv1d_layer(conv_input=out_MP1,
                    nbr_filters=1,
                    size_kernel=1,
                    step_stride=1,
                    type_padding="same",
                    activ_function=None)

  predicted_y_values = tf.reshape(out_CNfinal, tuple([minibatch_size,bin_seq_len//MP_mp_size, 1]))

  
  return predicted_y_values

#############################################################################################################################
############################################################################################################################# conv1d_model_CNs
#############################################################################################################################



def conv1d_model_CNs(CN_input,
                   CN_nbr_filters,
                   CN_size_kernel,
                   CN_step_stride,
                   CN_type_padding,
                   CN_activ_function,

                   minibatch_size, 
                   bin_seq_len, 
                   n_chip):

  from myutils_v2 import get_output_shape_convLayer
  from myutils_v2 import get_output_shape_poolLayer

  import tensorflow as tf

  nbr_CN_layers = len(CN_nbr_filters)
  assert nbr_CN_layers == len(CN_size_kernel)
  assert nbr_CN_layers == len(CN_step_stride)
  assert nbr_CN_layers == len(CN_type_padding)
  assert nbr_CN_layers == len(CN_activ_function)


  CN_output_size = []
  
  # initialize the input and input shape for CN1
  curr_CN_input = CN_input
  curr_CN_inshape = [minibatch_size, bin_seq_len, n_chip]
  
  for i_CN in range(nbr_CN_layers):
  
    ### CALL THE NN TO RETRIEVE THE PREDICTIONS
    out_CNi =  get_conv1d_layer(conv_input=CN_input,
                      nbr_filters=CN_nbr_filters[i_CN],
                      size_kernel=CN_size_kernel[i_CN],
                      step_stride=CN_step_stride[i_CN],
                      type_padding=CN_type_padding[i_CN],
                      activ_function=CN_activ_function[i_CN])
    # check the output of CN
    foo = tf.reshape(out_CNi, tuple([minibatch_size,bin_seq_len, CN_nbr_filters[i_CN]]))

    outCNi_size = get_output_shape_convLayer(
                      input_shape = curr_CN_inshape, 
                      kernel_size = CN_size_kernel[i_CN],
                      n_kernel = CN_nbr_filters[i_CN],
                      padding_type = CN_type_padding[i_CN].lower(),
                      stride_size = CN_step_stride[i_CN])
    CN_output_size += outCNi_size
    
    # UPDATE for next iteration
    curr_CN_input = out_CNi

    if CN_type_padding[i_CN]:
      curr_CN_inshape = [minibatch_size, bin_seq_len, CN_nbr_filters[i_CN]]                                                
    else:
      print("not implemented yet")
      sys.exit(1)
                                                     
  out_CNfinal = out_CNi                                                     
                                                     

#   print("outCN1_size = " + str(outCN1_size))  
#   print("outMP1_size = " + str(outMP1_size))
  
  predicted_y_values = tf.reshape(out_CNfinal, tuple([minibatch_size,bin_seq_len, 1]))
  
  return predicted_y_values

#############################################################################################################################
############################################################################################################################# loss_plot
#############################################################################################################################

def loss_plot(train_data, valid_data, image_file=None, plotTit=None):

  import matplotlib.pyplot as plt

  import numpy as np

  fig, axs = plt.subplots(1, 1, figsize=(10,8))
  ep_arr = np.arange(len(train_data))
  # axs.plot(ep_arr, all_epoch_loss_train, 'r')
  # axs.legend(('training loss'),  loc='upper right')
  axs.plot(ep_arr, train_data, 'r', ep_arr, valid_data, 'b')
  axs.legend(('epoch training loss', 'epoch valid loss'),  loc='upper right')

  if plotTit:
    plt.title(plotTit)
  if image_file:
    fig.savefig(image_file)   # save the figure to file

#############################################################################################################################
############################################################################################################################# print_in_file
#############################################################################################################################

def print_in_file(mytext, filename):
  with open(filename, 'a') as f:
    mytext += "\n"
    f.write(mytext)

