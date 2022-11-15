import os
import fit2gpx

# Use different libraries depending on the file type
def process_file(file_path):
    if file_path.endswith(".fit"):
        return process_fit_file(file_path)

# Convert fit file (which represents a segment) to a dataframe of coordinates
def process_fit_file(file_path):
    converter = fit2gpx.Converter()
    df_lap, df_points = converter.fit_to_dataframes(file_path)
    return df_points

# Takes a directory path and iterates over all files, returning a list of coordinate dataframes
def process_activity_files(directory):
    all_activities = []
    activity_files = os.scandir(directory)
    
    for file in activity_files:
        activity_dataframe = process_file(os.path.abspath(file))
        activity_dataframe["file_name"] = file.name

        all_activities.append(activity_dataframe)
    
    return all_activities

if __name__ == "__main__":
    file_list = process_activity_files("/workspaces/rad-routes/examples/activity_files/")
    print('Number of files processed: ' + str(len(file_list)))