#############################################################################
##                              DHLabel                                    ##
#############################################################################
# Command line tool to consolidate several DHL labels 
# for printing with less waste

import os
import sys
import argparse
import glob
from pypdf import PdfWriter, PdfReader, Transformation, PaperSize
from pypdf.generic import RectangleObject
from pypdf.annotations import FreeText
from datetime import date

#############################################################################
##                           Global variables                              ##
#############################################################################
input_path          = ""
output_path         = ""
today               = date.today().strftime("%Y-%m-%d")
output_files        = "DHLabels_" + today

#############################################################################
##                               Helpers                                   ##
#############################################################################

def argset():
    """
    Sets command line arguments
    """
    global input_path
    global output_path
    global output_files

    parser = argparse.ArgumentParser(description=
        "Command line tool to consolidate several DHL labels for printing with less waste")

    # Input path
    parser.add_argument('input_path', nargs='?', 
        default=os.getcwd(), 
        help="""
            Path to input PDFs. Will use current directory if ommited
            """)

    # Output path
    parser.add_argument('output_path', nargs='?', 
        default=os.getcwd(),
        help="""
            Path of output PDF and CSV. Will use 
            current directory if ommited
            """)

    # Parse args
    args = parser.parse_args()
    input_path  = args.input_path
    output_path = args.output_path

    # Output recognized args
    print("Using input path:")
    print(input_path)
    print("Using output path:")
    print(output_path)
    print("---")

    # Argument sanity checks
    if not os.path.isdir(input_path):
        print("The input path specified does not exist, exiting")
        sys.exit()
    if not os.path.isdir(output_path):
        print("The output path specified does not exist, exiting")
        sys.exit()

    # Assemble output file path without file extension
    output_files = os.path.join(output_path, output_files)


def read_file_list(input_path):
    """
    Read in files from input_path 
    """
    file_path_list = glob.glob(input_path + os.path.sep + "*.pdf")

    return(file_path_list)


def splice_files(file_path_list, output_files):
    """
    Create consolidated pdf
    """
    global today
    currentPage = 0
    national_file_path_list      = []
    international_file_path_list = []

    writer = PdfWriter()

    # Split into national / international labels by page count 
    # (Only international orders have the CN22/CN23 as a second page)
    for inputFile in file_path_list:
        reader = PdfReader(inputFile)

        if len(reader.pages) > 1:
            international_file_path_list.append(inputFile)
        else:
            national_file_path_list.append(inputFile)

    # Loop through international labels
    for inputFile in international_file_path_list:

        # Create and load readers/writers
        reader = PdfReader(inputFile)

        # Get recipient name from filename
        inputFileSplit = os.path.basename(inputFile).split("_")
        recipient = inputFileSplit[2] + " " + inputFileSplit[3].split(".")[0]

        # Collect pages
        pageAdress  = reader.pages[1]
        pageCN      = reader.pages[0]

        # Find tracking number in pdf text
        extractedText       = pageAdress.extract_text((0, 90))
        sendungsNummerPos   = extractedText.find("Sendungsnr.:")
        rightHalfText       = extractedText[sendungsNummerPos+13:]
        newLinePos          = rightHalfText.find("\n")
        sendungsNummer      = rightHalfText[:newLinePos]

        # Create a destination page
        destpage = writer.add_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)

        # Crop pages
        pageAdress.cropbox  = RectangleObject((0, (PaperSize.A4.height/2 + 20), PaperSize.A4.width, PaperSize.A4.height))
        pageCN.cropbox      = RectangleObject((0, (PaperSize.A4.height/2 + 20), PaperSize.A4.width, PaperSize.A4.height))

        # Merge pages down into destination
        destpage.merge_transformed_page(
                    pageAdress,
                    Transformation().translate(
                        0,
                        0,
                    ),
                )
        destpage.merge_transformed_page(
                    pageCN,
                    Transformation().translate(
                        0,
                        -PaperSize.A4.height/2+20,
                    ),
                )

        # Annotate current date into CN field
        annotation = FreeText(
            text=today,
            rect=(500, 50, 200, 100),
            font_color="000000",
            border_color=None,
            background_color=None
        )
        writer.add_annotation(page_number=currentPage, annotation=annotation)

        # Print successful recipient + Sendungsnummer
        print(recipient + " - (" + sendungsNummer + ")")

        # Append reportfile
        reportFile = output_files + ".csv"
        with open(reportFile, 'a') as rf:
            rf.write(recipient)
            rf.write(";")
            rf.write(sendungsNummer)
            rf.write(";\n")

        currentPage = currentPage + 1

    ### End looping through international labels

    

    # Loop through national labels
    currentPage = 0
    for inputFile in national_file_path_list:

        # Create and load readers/writers
        reader = PdfReader(inputFile)

        # Get recipient name from filename
        inputFileSplit = os.path.basename(inputFile).split("_")
        recipient = inputFileSplit[2] + " " + inputFileSplit[3].split(".")[0]

        # Collect pages
        pageAdress  = reader.pages[0]

        # Find tracking number in pdf text
        extractedText       = pageAdress.extract_text((0, 90))
        sendungsNummerPos   = extractedText.find("Sendungsnr.:")
        rightHalfText       = extractedText[sendungsNummerPos+13:]
        newLinePos          = rightHalfText.find("\n")
        sendungsNummer      = rightHalfText[:newLinePos]

        # Crop page
        pageAdress.cropbox  = RectangleObject((0, (PaperSize.A4.height/2 + 20), PaperSize.A4.width, PaperSize.A4.height))

        # On even pages (starting with 0):
        if (currentPage % 2) == 0:
            # Create a new destination page
            destpage = writer.add_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)
            # Merge page into upper part of dest page
            destpage.merge_transformed_page(
                    pageAdress,
                    Transformation().translate(
                        0,
                        0,
                    ),
                )
                
        # On uneven pages:
        else:
            # Merge page into lower part of dest page
            destpage.merge_transformed_page(
                    pageAdress,
                    Transformation().translate(
                        0,
                        -PaperSize.A4.height/2,
                    ),
                )

        # Print successful recipient + Sendungsnummer
        print(recipient + " - (" + sendungsNummer + ")")

        # Append reportfile
        reportFile = output_files + ".csv"
        with open(reportFile, 'a') as rf:
            rf.write(recipient)
            rf.write(";")
            rf.write(sendungsNummer)
            rf.write(";\n")

        currentPage = currentPage + 1

    ### End looping through national labels

    # Write resulting PDF
    outputname = output_files + ".pdf"
    with open(outputname, "wb") as op:
        writer.write(op)

    print("---")
    print("All files spliced")
    print("---")

#############################################################################
##                               main()                                    ##
#############################################################################
def main():
    print("--------------------")
    print("--Starting DHLabel--")
    print("--------------------")

    # Set command line arguments
    argset()

    # Read in file list
    file_path_list = read_file_list(input_path)

    # Check if files were found
    if not file_path_list:
        print("No valid files found at input_path, exiting")
        sys.exit()

    # Output file list
    print("Found the following files: ")
    for file in file_path_list:
        print(file)

    # Sanitize file list
    for file in file_path_list:
        if file == output_files + ".pdf":
            file_path_list.remove(file)

    print("---")
    
    # Output file list after sanitizing
    print("File list after sanitizing: ")
    for file in file_path_list:
        print(file)

    print("---")

    # Create spliced file
    splice_files(file_path_list, output_files)


#############################################################################
##                         main() idiom                                    ##
#############################################################################
if __name__ == "__main__":
    main()