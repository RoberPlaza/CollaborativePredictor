#!/usr/bin/env python3

import predictor
import models

import pandas as pd

from os import path
from os import listdir

predictors_directory    = "data/test/"
columns_to_estimate     = [ "CASOS", "Hospitalizados", "UCI", "Fallecidos", "Recuperados" ]

observations            = pd.read_csv( "data/observations_trimmed.csv" )
predictors              = [ predictor.Predictor( predictors_directory + dirent + "/" ) 
                           for dirent in sorted( listdir( predictors_directory ) )
                           if path.isdir( predictors_directory + dirent )]

## Comentar si ya hemos calculado los errores
for predictor in predictors:
    predictor.calculate_error_by_row( observations, columns_to_estimate )
    predictor.store_with_error_by_row()


collab_pred = models.CollaborativePredictor( predictors, observations )
collab_pred.assign_errors()
