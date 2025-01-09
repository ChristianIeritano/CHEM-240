import numpy as np

# Atomic masses dictionary
atomic_masses = {
    "H": 1.008, "C": 12.011, "O": 15.999, "N": 14.007, "S": 32.06,  # Add more if needed
}

def read_xyz(file_path):
    """
    Reads an XYZ file and returns atom types and coordinates.
    """
    atoms = []
    coordinates = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines[2:]:  # Skip the first two lines
            parts = line.split()
            if len(parts) == 4:
                atoms.append(parts[0])
                coordinates.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return atoms, np.array(coordinates)

def calculate_com(atoms, coordinates):
    """
    Calculate the center of mass of the structure.
    """
    total_mass = 0
    weighted_sum = np.zeros(3)
    for atom, coord in zip(atoms, coordinates):
        mass = atomic_masses[atom]
        total_mass += mass
        weighted_sum += mass * coord
    com = weighted_sum / total_mass
    return com

def translate_to_com(coordinates, com):
    """
    Translate all coordinates so that the center of mass is at (0, 0, 0).
    """
    return coordinates - com

def calculate_distances_to_com(coordinates):
    """
    Calculate the distance of each atom to the center of mass.
    """
    return np.linalg.norm(coordinates, axis=1)

def calculate_mass_weighted_distances(atoms, distances):
    """
    Calculate mass-weighted distances.
    """
    weighted_distances = []
    for atom, distance in zip(atoms, distances):
        mass = atomic_masses[atom]
        weighted_distances.append(mass * distance)
    return weighted_distances

def main(file_path):
    # Step 1: Read XYZ file
    atoms, coordinates = read_xyz(file_path)
    print("Step 1: Read atoms and coordinates:")
    for atom, coord in zip(atoms, coordinates):
        print(f"{atom}: {coord}")
    
    # Step 2: Calculate center of mass
    com = calculate_com(atoms, coordinates)
    print("\nStep 2: Center of Mass (COM):")
    print(com)
    
    # Step 3: Translate coordinates to make COM zero
    translated_coords = translate_to_com(coordinates, com)
    print("\nStep 3: Translated coordinates (COM at origin):")
    for atom, coord in zip(atoms, translated_coords):
        print(f"{atom}: {coord}")
    
    # Step 4: Calculate distances to the COM
    distances = calculate_distances_to_com(translated_coords)
    print("\nStep 4: Distances of atoms to COM:")
    for atom, distance in zip(atoms, distances):
        print(f"{atom}: {distance}")
    
    # Step 5: Calculate mass-weighted distances
    mass_weighted_distances = calculate_mass_weighted_distances(atoms, distances)
    print("\nStep 5: Mass-weighted distances:")
    for i, (atom, mw_distance) in enumerate(zip(atoms, mass_weighted_distances)):
        print(f"Atom {i} ({atom}): {mw_distance}")
    
    # Step 6: Sort mass-weighted distances with original indices
    indexed_distances = list(enumerate(mass_weighted_distances))
    sorted_distances = sorted(indexed_distances, key=lambda x: x[1])  # Sort by the mass-weighted distance
    print("\nStep 6: Sorted mass-weighted distances with original indices and atom identities:")
    for original_index, distance in sorted_distances:
        atom_identity = atoms[original_index]
        print(f"Atom {original_index} ({atom_identity}): {distance}")

# Run the script
xyz_file = r"C:\Users\ChristianIeritano\OneDrive - University of Waterloo\Waterloo\GitHub\CHEM-240\Module4\SS_Met-OMe_GM.xyz"
main(xyz_file)
