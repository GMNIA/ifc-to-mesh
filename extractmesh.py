import ifcopenshell
import ifcopenshell.geom
import os

def extract_mesh_from_ifc(ifc_file_path, output_dir):
    """
    Extract mesh data (vertices and faces) from IFC elements and save it.

    Args:
        ifc_file_path (str): Path to the IFC file.
        output_dir (str): Directory to save the mesh files.
    """

    # Set geometry settings (unit conversions and other options)
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    # Open the IFC file, create output directory if it doesn't exist
    ifc_file = ifcopenshell.open(ifc_file_path)
    os.makedirs(output_dir, exist_ok=True)

    # Extract geometry for each element of the ifc file
    print("Extracting mesh data...")
    for element in ifc_file.by_type("IfcProduct"):
        # Find data with correct attribute
        if not hasattr(element, "Representation") or not element.Representation:
            continue
        try:
            # Create shape geometry
            shape = ifcopenshell.geom.create_shape(settings, element)
            geometry = shape.geometry

            # Extract vertices and faces
            vertices = geometry.verts  # Flat list of vertex coordinates (x, y, z)
            faces = geometry.faces  # Flat list of indices forming triangular faces

            # Convert vertices into (x, y, z) tuples
            vertices_list = [
                (vertices[i], vertices[i + 1], vertices[i + 2])
                for i in range(0, len(vertices), 3)
            ]

            # Convert faces into triangle groups
            faces_list = [
                (faces[i], faces[i + 1], faces[i + 2])
                for i in range(0, len(faces), 3)
            ]

            # Save the mesh as an OBJ file
            obj_filename = os.path.join(output_dir, f"{element.is_a()}_{element.id()}.obj")
            with open(obj_filename, "w") as obj_file:
                # Write vertices
                for vertex in vertices_list:
                    obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

                # Write faces
                for face in faces_list:
                    obj_file.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")  # OBJ is 1-indexed
            print(f"Saved mesh for {element.is_a()} (ID: {element.id()}) to {obj_filename}")

        # Fail if there the mesh element is not valid
        except Exception as e:
            print(f"Failed to process element {element.is_a()} (ID: {element.id()}): {e}")


if __name__ == "__main__":
    # Path to the IFC file
    # ifc_file_path = "Ifc4_Revit_ARC.ifc"  # Replace with your IFC file path
    ifc_file_path = "examplestructure_test.ifc"  # Replace with your IFC file path

    # Output directory for mesh files
    output_dir = "midas"

    # Extract meshes
    extract_mesh_from_ifc(ifc_file_path, output_dir)

