#!/usr/bin/env python3

import numpy as np
import pandas as pd

from os import path
from os import listdir
from pathlib import Path

class Predictor:
    def __init__( self, dir_path :str ):
        self.user       = path.basename( path.normpath( dir_path ) )
        self.dir_path   = dir_path
        self.dfs        = []
        self.csv_names  = []
        
        for file in sorted( listdir( dir_path ) ):
            if path.isfile( dir_path + file ) and file.endswith( "csv" ):
                self.dfs.append( pd.read_csv( dir_path + file ) )
                self.csv_names.append( file )
                

    def calculate_error_by_row( self, experimental_values, columns, row_offset = 19 ):
        iterations = 0
        for df in self.dfs:
            for column in columns:
                df[ "{}_{}". format( column, "Error" ) ] = [ abs( df[ column ][ i ].astype( "int64" ) 
                                                            - experimental_values[ column ][ i + iterations* row_offset ].astype( "int64" ) )
                                                            for i in range(df.shape[ 0 ] ) ]
            iterations += 1 # Cada predicción tiene un offset de 19 por las comunidades autónomas

    def get_error_by_day( self ):
        return [ sum( row ) for row in self.get_error_by_day_and_row() ]

    
    def get_error_by_day_and_row( self ):
        return [ [  df[ column ].sum() for column in df.columns if "Error" in column ] for df in self.dfs ]
        
    def get_errors_of_columns( self, columns ):
        result = {}
        for column in columns:
            result[ column ] = []
            for df in self.dfs:
                result[ column ].append( np.array( df[ f"{column}_Error" ] ) )
        return result 

    def store_with_error_by_row( self, directory ):
        Path( directory + self.user ).mkdir( parents=True, exist_ok=True )
        for i in range( len( self.dfs ) ):
            file_name = directory + self.user + "/" + self.csv_names[ i ]
            self.dfs[ i ].to_csv( file_name, index = False )

    def __str__( self ):
        return self.user
