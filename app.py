import sys
from pathlib import Path

from camfixer.block_generator import block_generator
from camfixer.save_cam import save_cam
# from camfixer.es_pieza import es_pieza


def main():
    """Runs the main function."""
    OUTPUT_FILE = "output.cam"
    # Verificar si se proporcionó un archivo .CAM como argumento
    if len(sys.argv) != 2:
        print("Uso: python app.py archivo.cam")
        sys.exit(1)

    # Obtener el nombre del archivo .CAM proporcionado como argumento
    input_filepath = Path(sys.argv[1])
    print ("Archivo .CAM cargado correctamente.")

    block_gen = block_generator(input_filepath)

    blocks = list(block_gen)

    # es_pieza(blocks)


    # Save the blocks to a new file
    save_cam(blocks, OUTPUT_FILE)


if __name__ == "__main__":
    main()