import xml.dom.minidom as dom
import time
import os

print("   ____                                                   _           ___      _ _           _____  ")
print("  / ___|__ _ _ __   ___  ___ __ _ _ __  _ __   ___ _ __  | |_ ___    / _ \  __| (_)___      | ____| ")
print(" | |   / _` | '__| / __|/ __/ _` | '_ \| '_ \ / _ \ '__| | __/ _ \  | | | |/ _` | / __|_____|  _|   ")
print(" | |__| (_| | |    \__ \ (_| (_| | | | | | | |  __/ |    | || (_) | | |_| | (_| | \__ \_____| |___  ")
print("  \____\__,_|_|    |___/\___\__,_|_| |_|_| |_|\___|_|     \__\___/   \___/ \__,_|_|___/     |_____| ")
print("             a simple converter                                                            v.02 ENG ")                                            
print("                                                                        dontknowhowtocod3 & Mich795 ")
print(" ")
print("................................................................................................... ")
print(" ")

dataset_lc = []
dataset_information = []
diagnostic_address = ""
zdc_name = ""
zdc_version = ""
login = ""

def f_comma(my_str, group=2, char=',0x'):
    my_str = str(my_str)
    return char.join(my_str[i:i + group] for i in range(0, len(my_str), group))

def add_dataset():
    global diagnostic_address, zdc_name, zdc_version, login

    # Chiedi a quale centralina appartiene il dataset
    diagnostic_address_input = input("Which control unit does the dataset belong to? (Use only the last two characters i.e. 5F)\n")
    diagnostic_address = "0x" + diagnostic_address_input

    # Chiedi il nome del dataset
    zdc_name = input("Dataset name?\n")

    # Chiedi la versione del dataset
    while True:
        zdc_version_input = input("Dataset version? (Enter a number between 1 and 9999)\n")
        if zdc_version_input.isdigit() and 0 < int(zdc_version_input) <= 9999:
            zdc_version = zdc_version_input.zfill(4)
            break
        else:
            print("Invalid input. Try again.")

    # Chiedi il codice di sicurezza del dataset
    login = input("Dataset login code?\n")

    while True:
        dataset_address = input("Dataset address? (i.e. 0x000240)\n")
        dataset_lc.append(dataset_address)

        dataset_user = input("Dataset informations:\n")
        dataset_information.append("0x" + f_comma(dataset_user.upper()))

        choice = input("Want to add more? (Y/N)\n")
        if choice.upper() == "N":
            break

def missing_datasets():
    print("------------- ADDING MISSING DATASETS -------------\nTo exit press enter\n")
    while True:
        missing_dataset_lc = input("Select path where you want to save final dataset or press ENTER:\n")
        if missing_dataset_lc.upper() in dataset_lc:
            print(f"{missing_dataset_lc} It already exists! Please use a new name.")
            continue
        if missing_dataset_lc.rstrip() == "":
            print("Missing dataset information completed..")
            break
        else:
            print(f"Dataset {missing_dataset_lc} added to file!")
            dataset_lc.append(missing_dataset_lc.upper())
            new_ds = input("Insert dataset:\n")
            dataset_information.append("0x" + f_comma(new_ds.upper()))
            print("Dataset added!")

def printing_dataset():
    print("I'm generating final dataset...")

    # Crea l'oggetto documento
    doc = dom.Document()

    # Crea l'elemento radice
    root = doc.createElement("MESSAGE")
    doc.appendChild(root)

    # Imposta un attributo per l'elemento radice
    root.setAttribute("DTD", "XMLMSG")
    root.setAttribute("VERSION", "1.1")

    # Crea l'elemento result
    result = doc.createElement("RESULT")
    root.appendChild(result)

    # Crea l'elemento response
    response = doc.createElement("RESPONSE")
    result.appendChild(response)
    # Imposta gli attributi per l'elemento response
    response.setAttribute("NAME", "GetParametrizeData")
    response.setAttribute("DTD", "RepairHints")
    response.setAttribute("VERSION", "1.4.7.1")
    response.setAttribute("ID", "0")

    # Crea l'elemento data
    data = doc.createElement("DATA")
    response.appendChild(data)

    # Crea l'elemento request ID
    request_ID = doc.createElement("REQUEST_ID")
    data.appendChild(request_ID)

    # Imposta il testo per il sottoelemento
    req_id_text = doc.createTextNode("000002023")
    request_ID.appendChild(req_id_text)

    # Crea l'elemento PARAMETER_DATA
    for i in range(len(dataset_lc)):
        if dataset_information[i].strip() == "":
            continue
        parameter_data = doc.createElement("PARAMETER_DATA")
        data.appendChild(parameter_data)
        # Imposta gli attributi per l'elemento
        parameter_data.setAttribute("DIAGNOSTIC_ADDRESS", diagnostic_address)
        parameter_data.setAttribute("START_ADDRESS", dataset_lc[i])
        parameter_data.setAttribute("PR_IDX", "")
        parameter_data.setAttribute("ZDC_NAME", zdc_name)
        parameter_data.setAttribute("ZDC_VERSION", zdc_version)
        parameter_data.setAttribute("LOGIN", login)
        parameter_data.setAttribute("LOGIN_IND", "")
        parameter_data.setAttribute("DSD_TYPE", "1")
        parameter_data.setAttribute("SESSIONNAME", "")
        parameter_data.setAttribute("FILENAME", "")
        # Imposta il testo per l'elemento PARAMETER_DATA
        para_data_text = doc.createTextNode(str(dataset_information[i]))
        parameter_data.appendChild(para_data_text)

    # Crea l'elemento compounds
    for i in range(1, 6):
        compounds = doc.createElement("COMPOUNDS")
        data.appendChild(compounds)
        compound = doc.createElement("COMPOUND")
        compounds.appendChild(compound)
        compound.setAttribute("COMPOUND_ID", str(i))
        sw_name = doc.createElement("SW_NAME")
        compound.appendChild(sw_name)
        sw_version = doc.createElement("SW_VERSION")
        compound.appendChild(sw_version)
        sw_part_no = doc.createElement("SW_PART_NO")
        compound.appendChild(sw_part_no)

    # Crea l'elemento information
    information = doc.createElement("INFORMATION")
    data.appendChild(information)
    code_ = doc.createElement("CODE")
    information.appendChild(code_)

        # Crea l'elemento DSD_DATA
    dsd_data = doc.createElement("DSD_DATA")
    data.appendChild(dsd_data)

    compressed_data = doc.createElement("COMPRESSED_DATA")
    dsd_data.appendChild(compressed_data)
    dsd_data.setAttribute("CONTENT", "DSD-Files")
    dsd_data.setAttribute("CONTENT_TYPE", "application/tar")
    dsd_data.setAttribute("CONTENT_TRANSFER_ENCODING", "base64")
    dsd_data.setAttribute("BYTES_UNCOMPRESSED", "0")
    dsd_data.setAttribute("BYTES_COMPRESSED", "0")

    # Scrivi l'XML su un file
    xmlextension = "xml"
    while True:
        datasetgen = input("Enter a name for XML dataset file:\n")
        if datasetgen.strip() == "":
            print(f"No name entered, default name: {datasetgen}")
            datasetgen = "Dataset_ODIS-E"
        if os.path.exists(datasetgen + "." + xmlextension):
            print(f"File {datasetgen}.{xmlextension} already exists. Choose a different name.")
        else:
            with open(datasetgen + "." + xmlextension, "w", encoding="UTF-8") as f:
                f.write(doc.toprettyxml(indent="  ", encoding="UTF-8").decode())
                print("Dataset created successfully! Bye!")
                time.sleep(3)
                break

add_dataset()
missing_datasets()
printing_dataset()


