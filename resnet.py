#-*-coding:utf-8-*-


from keras.layers import Input, Add, Dense, Activation, Flatten, Conv3D, MaxPooling3D, ZeroPadding3D, \
    AveragePooling3D, BatchNormalization, TimeDistributed

from keras import backend as K

def identity_block(input_tensor, kernel_size, filters, stage, block, trainable=True):

    nb_filter1, nb_filter2, nb_filter3 = filters

    if K.image_dim_ordering() == 'tf':
        bn_axis == 4
    else:
        bn_axis == 1

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Conv3D(nb_filter1, (1,1,1), name=conv_name_base+'2a', trainable=trainable)(input_tensor)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base+'2a')(x)
    x = Activation('relu')(x)

    x = Conv3D(nb_filter2, (kernel_size, kernel_size, kernel_size), padding='same', name=conv_name_base+'2b', trainable=trainable)(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base+'2b')(x)
    x = Activation('relu')(x)

    x = Conv3D(nb_filter3, (1,1,1), name=conv_name_base+'2c', trainable=trainable)(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base+'2c')(x)

    x = Add()([x, input_tensor])
    x = Activation('relu')(x)

    return x


def identity_block_td(input_tensor, kernel_size, filters, stage, block, trainable=True):

    nb_filter1, nb_filter2, nb_filter3 = filters

    if K.image_dim_ordering() == 'tf':
        bn_axis == 4
    else:
        bn_axis == 1

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = TimeDistributed(Conv3D(nb_filter1, (1,1,1), trainable=trainable, kernel_initializer='normal'), name=conv_name_base+'2a')(input_tensor)
    x = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'2a')(x)
    x = Activation('relu')(x)

    x = TimeDistributed(Conv3D(nb_filter2, (kernel_size,kernel_size,kernel_size), padding='same', kernel_initializer='normal', trainable=trainable), name=conv_name_base+'2b')(x)
    x = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'2b')(x)
    x = Activation('relu')(x)

    x = TimeDistributed(Conv3D(nb_filter3, (1,1,1), trainable=trainable, kernel_initializer='normal'), name=conv_name_base+'2c')(x)
    x = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'2c')(x)

    x = Add()([x, input_tensor])
    x = Activation('relu')(x)

    return x


def conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2,2,2), trainable=True):

    nb_filter1, nb_filter2, nb_filter3 = filters

    if K.image_dim_ordering() == 'tf':
        bn_axis == 4
    else:
        bn_axis == 1

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = Conv3D(nb_filter1, (1,1,1), strides=strides, name=conv_name_base+'2a', trainable=trainable)(input_tensor)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base+'2a')(x)
    x = Activation('relu')(x)

    x = Conv3D(nb_filter2, (kernel_size,kernel_size,kernel_size), padding='same', 
        name=conv_name_base+'2b', trainable=trainable)(x)
    x = BatchNormalization(axis=bn_axis, name=bn_name_base+'2b')(x)
    x = Activation('relu')(x)

    x = Conv3D(nb_filter3, (1,1,1), name=conv_name_base+'2c', trainable=trainable)(x)
    x = BatchNormalization(axix=bn_axis, name=bn_name_base+'2c')(x)

    shortcut = Conv3D(nb_filter3, (1,1,1), strides=strides, name=conv_name_base+'1', trainable=trainable)(input_tensor)
    shortcut = BatchNormalization(axis=bn_axis, name=bn_name_base+'1')(shortcut)

    x = Add()([x, shortcut])
    x = Activation('relu')(x)

    return x


def conv_block(input_tensor, kernel_size, filters, stage, input_shape, block, strides=(2,2,2), trainable=True):

    nb_filter1, nb_filter2, nb_filter3 = filters

    if K.image_dim_ordering() == 'tf':
        bn_axis == 4
    else:
        bn_axis == 1

    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    x = TimeDistributed(Conv3D(nb_filter1, (1,1,1), strides=strides, trainable=trainable, kernel_initializer='normal'), 
        input_shape=input_shape, name=conv_name_base+'2a')(input_tensor)
    x = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'2a')(x)
    x = Activation('relu')(x)

    x = TimeDistributed(Conv3D(nb_filter2, (kernel_size,kernel_size,kernel_size), trainable=trainable,
        kernel_initializer='normal'), name=conv_name_base+'2b')(x)
    x = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'2b')(x)
    x = Activation('relu')(x)

    x = TimeDistributed(Conv3D(nb_filter3, (1,1,1), kernel_initializer='normal', trainable=trainable), 
        name=conv_name_base+'2c')(x)
    x = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'2c')(x)

    shortcut = TimeDistributed(Conv3D(nb_filter3, (1,1,1), strides=strides, trainable=trainable, kernel_initializer='normal'),
        name=conv_name_base+'1')(input_tensor)
    shortcut = TimeDistributed(BatchNormalization(axis=bn_axis), name=bn_name_base+'1')(shortcut)

    x = Add()([x, shortcut])
    x = Activation('relu')(x)

    return x


def nn_base(input_tensor=None, trainable=False):

    if K.image_dim_ordering() == 'th':
        input_shape = (1, None, None, None)
    else:
        input_shape = (None, None, None, 1)

    if input_shape is None:
        img_input = Input(shape=input_shape)

