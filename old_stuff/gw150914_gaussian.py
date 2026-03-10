import h5py
import numpy as np
f = h5py.File(data_folder / 'GW150914_data.h5')
dataset = f['overall_post']
dataset_dict = {}
for key in dataset.dtype.fields.keys():
    dataset_dict[key] = dataset[key]

dataset_dict['mchirp'] = (
    dataset_dict['mass1_det'] * dataset_dict['mass2_det']
    )**(3/5) / (dataset_dict['mass1_det'] + dataset_dict['mass2_det'])**(1/5)

dataset_dict['mtot'] = (
    dataset_dict['mass1_det'] + dataset_dict['mass2_det']
    )

units_errors = {
    'time': 's',
    'right_ascension': 'rad',
    'declination': 'rad',
    'theta_jn': 'rad',
}

for key in dataset_dict:
    data = dataset_dict[key]
    if key in units_errors:
        print(
            f'sigma_{key}: '
            f'{np.std(data):.3f} {units_errors[key]}'
        )
    else:
        print(
            f'sigma_{key} / {key}: '
            f'{np.std(data) / np.median(data):.3f}'
        )

region = ninety_percent_region(
        np.std(dataset_dict["right_ascension"]), 
        np.std(dataset_dict["declination"]), 
        np.cov(
            dataset_dict["right_ascension"],
            dataset_dict["declination"],
        )[0, 1], 
        np.median(dataset_dict["declination"]))

print(
    f'The 90% localization area for GW150914, in the Gaussian approximation, \n'
    f'is {region:.0f} square degrees, \n'
    'while the true one was approximately 600 square degrees'
)
