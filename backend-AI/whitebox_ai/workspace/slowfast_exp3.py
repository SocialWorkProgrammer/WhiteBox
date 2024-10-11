ann_file_test = 'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/annotation.txt'
ann_file_train = '/home/j-j11a104/data/1.Training/annotations/annotation.txt'
ann_file_val = '/home/j-j11a104/data/2.Validation/annotations/annotation.txt'
auto_scale_lr = dict(base_batch_size=32, enable=False)
data_root = 'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/'
data_root_val = '/home/j-j11a104/data/2.Validation/images_resize_bb/'
dataset_type = 'RawframeDataset'
default_hooks = dict(
    checkpoint=dict(
        interval=1, max_keep_ckpts=20, save_best='auto',
        type='CheckpointHook'),
    logger=dict(ignore_last=False, interval=20, type='LoggerHook'),
    param_scheduler=dict(type='ParamSchedulerHook'),
    runtime_info=dict(type='RuntimeInfoHook'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    sync_buffers=dict(type='SyncBuffersHook'),
    timer=dict(type='IterTimerHook'),
    visualization=dict(type='VisualizationHook'))
default_scope = 'mmaction'
env_cfg = dict(
    cudnn_benchmark=False,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
file_client_args = dict(io_backend='disk')
launcher = 'none'
load_from = 'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/best_acc_top1_epoch_94.pth'
log_level = 'INFO'
log_processor = dict(by_epoch=True, type='LogProcessor', window_size=20)
model = dict(
    backbone=dict(
        channel_ratio=8,
        fast_pathway=dict(
            base_channels=8,
            conv1_kernel=(
                5,
                7,
                7,
            ),
            conv1_stride_t=1,
            depth=50,
            lateral=False,
            norm_eval=False,
            pool1_stride_t=1,
            pretrained=None,
            type='resnet3d'),
        pretrained=None,
        resample_rate=8,
        slow_pathway=dict(
            conv1_kernel=(
                1,
                7,
                7,
            ),
            conv1_stride_t=1,
            depth=50,
            dilations=(
                1,
                1,
                1,
                1,
            ),
            inflate=(
                0,
                0,
                1,
                1,
            ),
            lateral=True,
            norm_eval=False,
            pool1_stride_t=1,
            pretrained=None,
            type='resnet3d'),
        speed_ratio=8,
        type='ResNet3dSlowFast'),
    cls_head=dict(
        average_clips='prob',
        dropout_ratio=0.5,
        in_channels=2304,
        num_classes=124,
        spatial_type='avg',
        type='SlowFastHead'),
    data_preprocessor=dict(
        format_shape='NCTHW',
        mean=[
            123.675,
            116.28,
            103.53,
        ],
        std=[
            58.395,
            57.12,
            57.375,
        ],
        type='ActionDataPreprocessor'),
    type='Recognizer3D')
optim_wrapper = dict(
    clip_grad=dict(max_norm=40, norm_type=2),
    optimizer=dict(
        amsgrad=False,
        betas=(
            0.9,
            0.999,
        ),
        eps=1e-08,
        lr=0.001,
        type='Adam',
        weight_decay=0.0001))
param_scheduler = [
    dict(
        begin=0,
        by_epoch=True,
        convert_to_iter_based=True,
        end=5,
        start_factor=0.01,
        type='LinearLR'),
    dict(
        T_max=95,
        begin=5,
        by_epoch=True,
        end=100,
        eta_min=1e-06,
        type='CosineAnnealingLR'),
]
resume = False
test_cfg = dict(type='TestLoop')
test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        ann_file=
        'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/annotation.txt',
        data_prefix=dict(
            img=
            'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/'
        ),
        pipeline=[
            dict(
                clip_len=32,
                frame_interval=2,
                num_clips=4,
                test_mode=True,
                type='SampleFrames'),
            dict(type='RawFrameDecode'),
            dict(scale=(
                -1,
                256,
            ), type='Resize'),
            dict(crop_size=224, type='CenterCrop'),
            dict(input_format='NCTHW', type='FormatShape'),
            dict(type='PackActionInputs'),
        ],
        test_mode=True,
        type='RawframeDataset'),
    num_workers=8,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
test_evaluator = [
    dict(
        out_file_path=
        'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/result.pkl',
        type='DumpResults'),
]
test_pipeline = [
    dict(
        clip_len=32,
        frame_interval=2,
        num_clips=4,
        test_mode=True,
        type='SampleFrames'),
    dict(type='RawFrameDecode'),
    dict(scale=(
        -1,
        256,
    ), type='Resize'),
    dict(crop_size=224, type='CenterCrop'),
    dict(input_format='NCTHW', type='FormatShape'),
    dict(type='PackActionInputs'),
]
train_cfg = dict(
    max_epochs=100, type='EpochBasedTrainLoop', val_begin=1, val_interval=1)
train_dataloader = dict(
    batch_size=16,
    dataset=dict(
        ann_file='/home/j-j11a104/data/1.Training/annotations/annotation.txt',
        data_prefix=dict(
            img=
            'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace/'
        ),
        pipeline=[
            dict(
                clip_len=32,
                frame_interval=2,
                num_clips=1,
                type='SampleFrames'),
            dict(type='RawFrameDecode'),
            dict(scale=(
                -1,
                256,
            ), type='Resize'),
            dict(
                input_size=224,
                max_wh_scale_gap=1,
                random_crop=True,
                scales=(
                    1,
                    0.875,
                    0.75,
                    0.66,
                ),
                type='MultiScaleCrop'),
            dict(keep_ratio=False, scale=(
                224,
                224,
            ), type='Resize'),
            dict(flip_ratio=0.5, type='Flip'),
            dict(input_format='NCTHW', type='FormatShape'),
            dict(type='PackActionInputs'),
        ],
        type='RawframeDataset'),
    num_workers=8,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='DefaultSampler'))
train_pipeline = [
    dict(clip_len=32, frame_interval=2, num_clips=1, type='SampleFrames'),
    dict(type='RawFrameDecode'),
    dict(scale=(
        -1,
        256,
    ), type='Resize'),
    dict(
        input_size=224,
        max_wh_scale_gap=1,
        random_crop=True,
        scales=(
            1,
            0.875,
            0.75,
            0.66,
        ),
        type='MultiScaleCrop'),
    dict(keep_ratio=False, scale=(
        224,
        224,
    ), type='Resize'),
    dict(flip_ratio=0.5, type='Flip'),
    dict(input_format='NCTHW', type='FormatShape'),
    dict(type='PackActionInputs'),
]
val_cfg = dict(type='ValLoop')
val_dataloader = dict(
    batch_size=32,
    dataset=dict(
        ann_file='/home/j-j11a104/data/2.Validation/annotations/annotation.txt',
        data_prefix=dict(
            img='/home/j-j11a104/data/2.Validation/images_resize_bb/'),
        pipeline=[
            dict(
                clip_len=32,
                frame_interval=2,
                num_clips=1,
                test_mode=True,
                type='SampleFrames'),
            dict(type='RawFrameDecode'),
            dict(scale=(
                -1,
                256,
            ), type='Resize'),
            dict(crop_size=224, type='CenterCrop'),
            dict(input_format='NCTHW', type='FormatShape'),
            dict(type='PackActionInputs'),
        ],
        test_mode=True,
        type='RawframeDataset'),
    num_workers=8,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
val_evaluator = [
    dict(
        metric_list=(
            'top_k_accuracy',
            'mean_class_accuracy',
        ),
        metric_options=dict(top_k_accuracy=dict(topk=(
            1,
            5,
        ))),
        type='AccMetric'),
    dict(type='ConfusionMatrix'),
]
val_pipeline = [
    dict(
        clip_len=32,
        frame_interval=2,
        num_clips=1,
        test_mode=True,
        type='SampleFrames'),
    dict(type='RawFrameDecode'),
    dict(scale=(
        -1,
        256,
    ), type='Resize'),
    dict(crop_size=224, type='CenterCrop'),
    dict(input_format='NCTHW', type='FormatShape'),
    dict(type='PackActionInputs'),
]
vis_backends = [
    dict(type='LocalVisBackend'),
]
visualizer = dict(
    type='ActionVisualizer', vis_backends=[
        dict(type='LocalVisBackend'),
    ])
work_dir = 'C:/Users/SSAFY/Desktop/final/S11P21A104/backend-AI/whitebox_ai/workspace'
