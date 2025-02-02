import os
import sys
import extractmesh
import convertmidas

def main():
    # Define file paths
    ifc_file = "example-structure.ifc"
    output_dir = "midas"

    # Ensure input file exists
    if not os.path.isfile(ifc_file):
        print(f"Error: IFC file '{ifc_file}' not found.")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Extract Mesh from IFC
    print("\nStep 1: Extracting mesh from IFC...")
    extractmesh.extract_mesh_from_ifc(ifc_file, output_dir)

    # Check if OBJ files were created
    obj_files = [f for f in os.listdir(output_dir) if f.endswith(".obj")]
    if not obj_files:
        print("Error: No OBJ files were generated from the IFC file.")
        sys.exit(1)

    # Step 2: Convert OBJ to MCT
    print("\nStep 2: Converting OBJ files to MCT format...")
    for obj_file in obj_files:
        obj_file_path = os.path.join(output_dir, obj_file)
        convertmidas.convert_obj_to_mct(obj_file_path, output_dir)

    print("\nConversion complete. MCT files are saved in the 'midas' folder.")

if __name__ == "__main__":
    main()
