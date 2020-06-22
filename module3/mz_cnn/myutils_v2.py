def get_output_shape_convLayer(input_shape, 
                       kernel_size,
                       n_kernel,
                       padding_type="same", 
                       stride_size=1, 
                              verbose=False):
  
  in_width, in_height, in_dim = tuple(input_shape)
  
  
  if verbose:
    print("input: \t" + str(in_width) + " x " + str(in_height) + " x " + str(in_dim))
  
  # 1x12x1 - 3x1 -> 1x10x1
  # 1x12x1 - 5x1 -> 1x8x1
  kernel_dim = in_dim
  
  out_dim = n_kernel
  
  if padding_type.lower() == "same":
    out_width, out_height = in_width/stride_size, in_height/stride_size
  
  elif padding_type.lower() == "valid":
    pad_size = 0
    out_width = in_width
    out_height = (in_height - kernel_size + 2*pad_size)/stride_size + 1
    
  else:
    sys.exit(1)
    
  if verbose:  
    print("output: \t" + str(out_width) + " x " + str(out_height) + " x " + str(out_dim))
  
  return [out_width, out_height, out_dim]

  
  
# get_output_shape_convLayer(input_shape = [1,12,3],
#                   kernel_size = 5,
#                   n_kernel = 1,
#                   padding_type = "valid",
#                   stride_size = 1)

####################################################################################
####################################################################################
####################################################################################

def get_output_shape_poolLayer(input_shape, 
                       pool_size=2,
                      stride_size = 1, 
                               verbose = False):
    
  in_width, in_height, in_dim = tuple(input_shape)
  
  if verbose:
    print("input: \t" + str(in_width) + " x " + str(in_height) + " x " + str(in_dim))


  if verbose:
    print("in_width: \t" + str(in_width))
        
  # 1x12x1 - 3x1 -> 1x10x1
  # 1x12x1 - 5x1 -> 1x8x1
  
  out_width = (in_width - pool_size)/stride_size + 1
  
  if out_width == 0:
    out_width = 1

  if verbose:
    print("out_width: \t" + str(out_width))
  
  
  out_height = (in_height - pool_size)/stride_size + 1
  if out_height == 0:
    out_height = 1
  
  
  out_dim = in_dim
    
  if verbose:
    print("output: \t" + str(out_width) + " x " + str(out_height) + " x " + str(out_dim))

  return [out_width, out_height, out_dim]

  
get_output_shape_poolLayer(input_shape = [1,12,1],
                  pool_size = 1,
                  stride_size = 1,
                  verbose=True)


