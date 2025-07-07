from PyPDF2 import PdfMerger

def fusionner_pdfs(paths, output_path):
    """
    Fusionne une liste de fichiers PDF en un seul fichier.

    :param paths: Liste des chemins vers les fichiers PDF à fusionner
    :param output_path: Chemin du PDF de sortie
    """
    merger = PdfMerger()
    for path in paths:
        merger.append(path)
    merger.write(output_path)
    merger.close()
