import subprocess
import os

Root_folder = "thesis_minor" #Change each new project
name_genref = "sequence"
name_index_genref = "Mbovis"
## Path to output files
path_raw_data = f"/home/albertdalmau/{Root_folder}/datasets/Raw_data"
path_output_fastqc = f"/home/albertdalmau/{Root_folder}/datasets/fast_outputs"
path_output_cutadapt = f"/home/albertdalmau/{Root_folder}/datasets/cutad_outputs"
path_adapters = f'/home/albertdalmau/{Root_folder}/python_scripts/adapters.fasta'
path_output_align = f"/home/albertdalmau/{Root_folder}/datasets/bowtie_outputs/mapping"
path_bam_files = f"/home/albertdalmau/{Root_folder}/datasets/bowtie_outputs/bam_files"
path_sorted_bamfiles = f"/home/albertdalmau/{Root_folder}/datasets/bowtie_outputs/sorted_bamfiles"
path_sorted_bamfiles_w = "/mnt/c/Users/tarca/OneDrive/Documentos/Internship_Josemari/DEA/Datasets/Sorted_bamfiles"
path_counts_output = f"/home/albertdalmau/{Root_folder}/datasets/counts_outputs"
path_counts_output_w = "/mnt/c/Users/tarca/OneDrive/Documentos/Internship_Josemari/DEA/Datasets/Counts"
path_counts_output_w_short = "/mnt/c/Users/tarca/OneDrive/Documentos/Internship_Josemari/DEA/Short_counts"
## Paths to reference genome 
path_folder_refgen = f"/home/albertdalmau/{Root_folder}/datasets/Reference_genome"
path_refgen_fasta = f'/home/albertdalmau/{Root_folder}/datasets/Reference_genome/{name_genref}.fasta'
index_genref = f"/home/albertdalmau/{Root_folder}/datasets/Reference_genome/index/{name_index_genref}"
anot_file_path = f"/home/albertdalmau/{Root_folder}/datasets/Reference_genome/{name_genref}.gff" 
#Path to load samtools
samtools = "/home/albertdalmau/thesis_minor/programs/samtools/bin/samtools" 

#PARAMETERS TRIMMING  
THR_SHORT_FRAG = "30"  # Get rid of the short fragments
THR_BAD_FRAG = "25"    # Quality score
THR_TRIM_SIDE = "16"   # Based on per base sequence content 
#-----------------------------------------------------------------------------------------------------------------------------------
def file_names_list(folder_path):
    '''Return the path of the files inside a folder in list format separated by commas'''
    ## Get the names of the files as strings
    if folder_path == path_output_align:
        all_files_paths = subprocess.run(f'ls {folder_path}/*.sam', capture_output=True, text=True, shell=True)
    elif folder_path == path_bam_files or folder_path == path_sorted_bamfiles:
        all_files_paths = subprocess.run(f'ls {folder_path}/*.bam', capture_output=True, text=True, shell=True)
    elif folder_path == path_counts_output_w:
        all_files_paths = subprocess.run(f'ls {folder_path}/*.txt', capture_output=True, text=True, shell=True)
    else:
        all_files_paths = subprocess.run(f'ls {folder_path}/*.fastq', capture_output=True, text=True, shell=True)
    ## Split the output into lines
    all_files = all_files_paths.stdout.splitlines() #This command makes each line to be an element of a list
    return all_files

def file_names_str(folder_path):
    '''Return the path of the files inside a folder in string format separated by a space'''
    all_files = file_names_list(folder_path)
    filenames = " ".join(all_files)                 #Convert the list in a string separated by ' '.
    return filenames
 
#-----------------------------------------------------------------------------------------------------------------------------------
if input("Would you like to perform quality check and trimming of the data? (type YES or NO): ").lower()=="yes":
### 1.- FASTQC (quality check)
        ## Run the files and store the output (remember that the input file needs to have all the path)
    if input("Would you like to perform fastQC analysis? (type YES or NO): ").lower() == "yes":
        subprocess.run(['fastqc', file_names_str(path_raw_data), '-o' , path_output_fastqc], capture_output=True, text=True)
        print("FastQC successfully executed")

    ### 2.- CUTADAPT (trimming)
    if input("Would you like to trim low-quality sequences (CutAdapt)? type YES or NO: ").lower() == "yes":
        for file_path in file_names_list(path_raw_data):
            #set outputs names (by expanding the path of the directory):
            base_samplenames = os.path.basename(file_path) #gets only the name of the file
            trim_output=os.path.join(path_output_cutadapt,f'trimmed_{base_samplenames}')  #define the output
            #run cutadapt:
            subprocess.run(["cutadapt", "-q", THR_BAD_FRAG,  # Quality threshold
                            '-m', THR_SHORT_FRAG,            # Minimum fragment length
                            '-u', THR_TRIM_SIDE,             # Trim 16 bases from the 5' end
                            '-u', f'-{THR_TRIM_SIDE}',       # Trim 16 bases from the 3' end
                            "-b", f'file:{path_adapters}',   # Adapter trimming (checks 3' and 5' ends)
                            "-o", trim_output, file_path     # Output and input files
                            ], capture_output=True, text=True)
            #break # REMEBER TO TAKE IT OUT!
        print("Trimming successfully executed")

#-----------------------------------------------------------------------------------------------------------------------------------
if input("Would you like to perform the alignment? (type YES or NO): ").lower()=="yes":
### 3.- BOWTIE2 (alignment)   
    if input ("Would you like to index the reference genome? type YES or NO: ").lower()=="yes":
        subprocess.run(['mkdir', '-p', f'{path_folder_refgen}/index'])
        print("index folder created")
        subprocess.run(['bowtie2-build', path_refgen_fasta, f'{path_folder_refgen}/index/Mbovis'], capture_output=True, text=True)
        print("Referene genome has been indexed")

    if input ("Would you like to perfrom the mapping? type YES or NO: ").lower()=="yes": 
        for file_path in file_names_list(path_output_cutadapt):
            #set outputs names (by expanding the path of the directory):
            base_samplenames = os.path.splitext(os.path.basename(file_path))[0] #split.text -> split into base name and extension (.fastq)
                                                                                # this output is a tupple, thats why we need [0]
            bowtie_output = os.path.join(path_output_align,f'{base_samplenames}.sam')
            
            res_alig = subprocess.run(["bowtie2", "-x", index_genref, "-U", file_path, "-S", bowtie_output, "--threads 6"], 
                                    capture_output=True, text=True)
            print(res_alig.stdout)
            #break
        print("Alignment successfully executed")

### 4.- CONVERSION .sam -> .bam file
    if input ("Would you like to convert .sam to .bam files? type YES or NO: ").lower()=="yes":
        for file_path in file_names_list(path_output_align):
            base_samplenames = os.path.splitext(os.path.basename(file_path))[0]  
            sam_output = os.path.join(path_bam_files,f'{base_samplenames}.bam')
            subprocess.run([samtools, "view", "-b", "-o", sam_output, file_path], capture_output=True, text=True)
        print('Conversion successfully executed')

### 5.- SAMTOOLS STATISTICS
    while True:
        response = input("Would you like to check the mapping statistics? type YES or NO: ").lower()
        if response == "yes":
            file = input("Enter the file you would like to check: ")
            file_to_check = os.path.join(path_bam_files, file)
            result_stats = subprocess.run([samtools, 'flagstat', file_to_check], capture_output=True, text=True)
            print(result_stats.stdout)
        elif response == "no":
            print('Statistics checking skipped.')
            break  
        else:
            print("Invalid response. Please type YES or NO.")

### 6.- SORTING .bam files
    if input ("Would you like to sort the .bam file? type YES or NO: ").lower()=="yes":
        for file_path in file_names_list(path_bam_files):
            base_samplenames = os.path.basename(file_path) #gets only the name of the file
            sorted_output = os.path.join(path_sorted_bamfiles,f'sorted_{base_samplenames}')
            sorted_output_w = os.path.join(path_sorted_bamfiles_w, f'sorted_{base_samplenames}')
            subprocess.run([samtools,'sort', '-@', '6', '-o', sorted_output, file_path], capture_output=True, text=True)
            subprocess.run([samtools,'sort', '-@', '6', '-o', sorted_output_w, file_path], capture_output=True, text=True)
        print("Sorting successfully executed")

### 7.- INDEXING .bam files for IGV visualizayion
    if input ("Would you like to index the .bam file for igv visualization? type YES or NO: ").lower()=="yes":
        for file_path in file_names_list(path_sorted_bamfiles):
            subprocess.run([samtools, 'index', file_path], capture_output=True, text=True)
    print("Indexing of the .bam file successfully executed")

#-----------------------------------------------------------------------------------------------------------------------------------
if input("Would you like to obtain mRNA's counts? (type YES or NO): ").lower()=="yes":
### 8.- RNA-seq count matrix 
    if input ("Would you like to obtain the whole counting data? type YES or NO: ").lower()=="yes":
        for file_path in file_names_list(path_sorted_bamfiles):
                base_samplenames=os.path.splitext(os.path.basename(file_path))[0] 
                count_out=os.path.join(path_counts_output, f'counts_{base_samplenames}.txt')
                count_out_w=os.path.join(path_counts_output_w, f'counts_{base_samplenames}.txt')
                res_c = subprocess.run(["featureCounts", 
                                        "-T", "6",  # Number of threads
                                        "-g", "locus_tag",  # GTF attribute type
                                        "-a", anot_file_path,  # Annotation file (GTF)
                                        "-t", "gene",  # Feature type (GTF)
                                        "-o", count_out,  # Output file
                                        file_path  # Input BAM file
                                                                    ])
                subprocess.run(["featureCounts", "-T", "6", "-g", "locus_tag", "-a", anot_file_path, "-t", "gene",
                                 "-o", count_out_w, file_path])

    if input("Would you like to reduce the RNA-seq count matrix? type YES or NO: ").lower() == "yes":
        for file_path in file_names_list(path_counts_output_w):
            output_file = f"{path_counts_output_w_short}/{file_path.split('/')[-1].replace('.txt', '_reduced.txt')}"
            # Open the output file and process the command
            with open(output_file, 'w') as f:
                process1 = subprocess.Popen(['cat', file_path], stdout=subprocess.PIPE, text=True)
                process2 = subprocess.Popen(['cut', '-f1,7'], stdin=process1.stdout, stdout=f, text=True)
                process1.stdout.close()  # Allow process1 to receive a SIGPIPE if process2 exits
                process2.wait()  # Wait for process2 to complete
    else:
        print("Reducing skipped")

    if input("Would you like to check the summary? type YES or NO: ").lower() == "yes":
        file_counts = input ('Enter the file to check: ')
        subprocess.run(['cat', 'demo', os.path.join(path_counts_output,file_counts)])

        

