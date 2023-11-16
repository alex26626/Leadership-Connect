# Leadership-Connect
This file is a guideline to the codes and the files which can be found in the "Code" folder. Additional details and comments about the functions are in the specific Python files.
1)	Panel_Function.py: this file contains a single function, to be used to panelize the datasets downloaded from the Leadership Connect site.
2)	Descriptive_Statistics_Functions.py: this file contains three functions:
a)	null_perc(d): this function computes the percentage of null observations for each column of the dataset.
b)	stats(d, column): this function computes the relative frequency of observations for each category of the specified column.
c)	top_30(data): this function returns the absolute and relative frequencies of the top 30 observations for each column of the specified dataset.
3)	Web_Scraping.py: this file contains functions to be used to download images and their relative information from either Google Images or LinkedIn:
a)	download_n(names, folder, n, destination_name): this function allows to download images from Google Images. Furthermore, it generates a file, where, for each downloaded image, the following attributes are provided:
-	File Name: the name with which the downloaded image is saved.
-	The src code of the image, which is a unique identifier allowing for the download of the image.
-	Origin: The source from which the image is downloaded.
b)	linkedin_scraping(email, password_text, names): the following function allows to download images from LinkedIn. It looks for at most 5 images for each person. It returns three outputs:
-	all_names: The list of the names of the downloaded images.
-	all_images: The list of src codes of the images.
-	all_experiences: The list of working experiences for each searched person.
NB: The order across the three lists is consistent.
c)	exp_cleaning(all_experiences): this function cleans the list of experiences provided by the linkedin_scraping function. It takes the list of experiences as an input, and it outputs the list of cleaned experiences. The order is preserved.
d)	link_data(all_names, all_experiences, all_images): The following function generates a dataframe with the outputs obtained from the linkedin_scraping function:
-	Code Name: The specific name of the downloaded image (ex. Name_Surname_0.jpg).
-	Full Name: The full name of the person in the image (ex. Name_Surname).
-	Image: The src code of the image.
-	Experience: The working experience of the person in the image.
4)	Comparisons_Origins.py: this file contains the functions which are used to evaluate the accuracy of the images downloaded through web scraping, and the reliability of the sources from which the images are downloaded.
a)	match_rates(data_set): this function takes a comparison dataset as an input, and it prints the following match rates:
-	% of positive pairs: The % of names for which at least one downloaded image is correct.
-	% of negative pairs: The % of names for which none of the downloaded images is correct.
-	Average Prediction: Considering only positive pairs, it's the average number of correct images per person.
-	Percentage of first predictions: Considering only positive pairs, it's the % of times the first downloaded image is correct.
b)	sub_match_rates(combination_directory, comparison_directory, threshold): The following function computes and prints the match rates defined above for majority voting. It takes as inputs:
-	combination_directory: The directory to the combination file.
-	comparison_directory: The directory to the comparison file.
-	threshold: The threshold for majority voting. For instance, if threshold = 3, then the match rates will be computed only for names for which at least 3 among the downloaded images are the same (contain the same person).
In addition to the match rates defined above, the function also computes the Sample Proportion, which is the percentage of names left after applying the threshold. For instance, if threshold = 3, and Sample Proportion = 30%, then for 30% of the people at least 3 images are the same (contain the same person).
c)	origins_analysis(origins_data, comparisons_data): this function takes as inputs an origin dataset and a comparison dataset, and it outputs three graphs:
-	Positive Origins: The most frequent sources among positive pairs, in decreasing order, with their relative frequency.
-	Negative Origins: The most frequent sources among negative pairs, in decreasing order, with their relative frequency.
-	Null Origins: The most frequent sources among null pairs (where the downloaded image is not a person), in decreasing order, with their relative frequency.
The Comparison_Combination_Origin_Files.zip folder contains the files to be used as inputs for the functions in the Comparisons_Origins.py file. All the information in these files refers to images downloaded from Google Images. There are three different types of files: comparison files, combination files, and origin files, which are to be used as defined by the inputs names in the functions. Furthermore, there are different sub-categories depending on the name: 
1)	The number in the file name refers to the number of images downloaded per each person. For instance, if the file name contains 10, then it refers to the case of the first 10 images downloaded per each person. 
2)	The first half of the name refers to the inputs used in the search bar:
  a)	Standard refers to using only first_name + last_name.
  b)	LinkedIn refers to using first_name + last_name + LinkedIn.
  c)	LinkedIn_Law refers to using first_name + last_name + LinkedIn + Law.
  d)	LinkedIn_Title refers to using first_name + last_name + LinkedIn + job_title.
Important: when using such files as inputs for the functions, it’s essential to use files containing the same number and the same type of input in the search bar.  For instance origins_analysis(Standard_10_Origins.csv, Standard_10_Comparison.csv), will refer to the case of 10 images downloaded per person, using only first and last name in the search bar. 
