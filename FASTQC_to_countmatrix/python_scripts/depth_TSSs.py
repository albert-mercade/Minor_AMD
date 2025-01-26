import subprocess
import os


#Parameters
Root_folder = "thesis_minor" #Change each new project
name_genref = "sequence"

#Path to load samtools
samtools = "/home/albertdalmau/thesis_minor/programs/samtools/bin/samtools" 

#Path to different files
path_sorted_bamfiles = f"/home/albertdalmau/{Root_folder}/datasets/bowtie_outputs/sorted_bamfiles"

#----------------------------------------------------------------------------------------------------------------
def file_names_list(folder_path):
    '''Return the path of the files inside a folder in list format separated by commas'''
    ## Get the names of the files as strings
    if folder_path == path_sorted_bamfiles:
        all_files_paths = subprocess.run(f'ls {folder_path}/*.bam', capture_output=True, text=True, shell=True)
    ## Split the output into lines
    all_files = all_files_paths.stdout.splitlines() #This command makes each line to be an element of a list
    return all_files

def file_names_str(folder_path):
    '''Return the path of the files inside a folder in string format separated by a space'''
    all_files = file_names_list(folder_path)
    filenames = " ".join(all_files)                 #Convert the list in a string separated by ' '.
    return filenames

#------------------------------------------------------------------------------------------------------------------
if input("Would you like to obtain the depth of the files? (type YES or NO): ").lower() == 'yes':
    for file_path in file_names_list(path_sorted_bamfiles):
        if "cap" in file_path:
            output_name = os.path.splitext(os.path.basename(file_path))[0] 
            path_output_depth = f"/home/albertdalmau/{Root_folder}/datasets/TSSmap/depth/depth_{output_name}.txt"
            path_output_depth_w = f"/mnt/c/Users/tarca/OneDrive/Documentos/Internship_Josemari/TSS/depth/depth_{output_name}.txt"
            output_paths_depth = [path_output_depth, path_output_depth_w]
            
            for output_path in output_paths_depth:
                with open(output_path, "w") as f:  # Open each output file
                    output = subprocess.run([samtools, "depth", "-a", file_path], stdout=f, text=True)
    
    print('Depth successfully obtained')







