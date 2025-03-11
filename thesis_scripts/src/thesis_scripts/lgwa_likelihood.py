from .lunar_coordinates import (
    generate_data_position, 
    generate_data_response, 
    spherical_to_cartesian,
    wave_frame_basis_cartesian
)
from . import data_path
import logging
import numpy as np
from scipy.interpolate import interp1d

class LunarLikelihood:
    
    def __init__(self, gps_time_range=(1577491218., 1893024018.)):
        
        self.gps_time_range = gps_time_range
        self.cache_folder = data_path / 'cache'
        self.ensure_ephemeris_are_available()
    

    def get_detector_frame(self, time):
        n_ra = np.interp(time, self.times_response, self.data_response[:, 0])
        n_dec = np.interp(time, self.times_response, self.data_response[:, 1])
        x_ra = np.interp(time, self.times_response, self.data_response[:, 2])
        x_dec = np.interp(time, self.times_response, self.data_response[:, 3])
        y_ra = np.interp(time, self.times_response, self.data_response[:, 4])
        y_dec = np.interp(time, self.times_response, self.data_response[:, 5])

        return (
            spherical_to_cartesian(n_ra, n_dec),
            spherical_to_cartesian(x_ra, x_dec),
            spherical_to_cartesian(y_ra, y_dec),
        )
    
    def get_antenna_response(self, time, ra, dec, psi):
        
        n, x, y = self.get_detector_frame(time)
        
        u, v = wave_frame_basis_cartesian(ra, dec, psi)
        
        un = np.dot(n, u)
        ux = np.dot(x, u)
        uy = np.dot(y, u)
        vn = np.dot(n, v)
        vx = np.dot(x, v)
        vy = np.dot(y, v)

        hp1 = un * ux - vn * vx
        hc1 = un * vx + vn * ux
        hp2 = un * uy - vn * vy
        hc2 = un * vy + vn * uy

        return hp1, hp2, hc1, hc2
    
    def get_detector_position(self, time):
        
        x = np.interp(time, self.times_position, self.data_position[:, 0])
        y = np.interp(time, self.times_position, self.data_position[:, 1])
        z = np.interp(time, self.times_position, self.data_position[:, 2])
        
        return np.asarray([x, y, z])
    
    def ensure_ephemeris_are_available(self):
        
        fname_times_position = (self.cache_folder / 'times_position').with_suffix('.npy')
        fname_times_response = (self.cache_folder / 'times_response').with_suffix('.npy')
        fname_data_position = (self.cache_folder / 'data_position').with_suffix('.npy')
        fname_data_response = (self.cache_folder / 'data_response').with_suffix('.npy')
        
        if fname_data_position.exists() and fname_times_position.exists():
            self.times_position = np.load(fname_times_position)
            self.data_position = np.load(fname_data_position)
        else:
            logging.info('Computing position interpolant')
            n_points_position = int((self.gps_time_range[1]-self.gps_time_range[0]) / (60*15))
            self.times_position, self.data_position = generate_data_position(n_points_position, *self.gps_time_range)
            np.save(fname_times_position, self.times_position.value)
            np.save(fname_data_position, self.data_position)
            
        if fname_data_response.exists() and fname_times_response.exists():
            self.times_response = np.load(fname_times_response)
            self.data_response = np.load(fname_data_response)
        else:
            logging.info('Computing response interpolant')            
            n_points_response = int((self.gps_time_range[1]-self.gps_time_range[0]) / (60*250))
            self.times_response, self.data_response = generate_data_response(n_points_response, *self.gps_time_range)
            np.save(fname_times_response, self.times_response.value)
            np.save(fname_data_response, self.data_response)
            

if __name__ == '__main__':
    like = LunarLikelihood((1500000000., 2000000000.))
    t0 = 1577491218.
    times = np.linspace(t0, t0+100000, num=10)
    print(like.get_antenna_response(time=times, ra=0, dec=90, psi=0))
    # LunarLikelihood((1500000000., 1500110000.))
    