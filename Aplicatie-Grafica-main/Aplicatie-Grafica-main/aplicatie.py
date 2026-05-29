import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import json
import math
import os
from tkinter import Tk, filedialog, messagebox

class Point3D:
    def __init__(self, x, y, z, name="", color=(1, 1, 1)):
        self.pos = np.array([x, y, z], dtype=float)
        self.name = name
        self.color = color
        self.selected = False

class Edge:
    def __init__(self, p1_idx, p2_idx, color=(0.7, 0.7, 0.7)):
        self.p1_idx = p1_idx
        self.p2_idx = p2_idx
        self.color = color

class Face:
    def __init__(self, indices, color=(0.5, 0.5, 0.8)):
        self.indices = indices
        self.color = color

class Camera:
    def __init__(self):
        self.distance = 10.0
        self.yaw = 0.0
        self.pitch = 30.0
        self.target = np.array([0.0, 0.0, 0.0])
        
    def apply(self):
        glLoadIdentity()
        x = self.distance * math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw))
        y = self.distance * math.sin(math.radians(self.pitch))
        z = self.distance * math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
        gluLookAt(x, y, z, self.target[0], self.target[1], self.target[2], 0, 1, 0)

class Scene3D:
    def __init__(self):
        self.points = []
        self.edges = []
        self.faces = []
        self.camera = Camera()
        self.selected_point = None
        self.render_mode = 'solid'
        self.light_position = [5.0, 5.0, 5.0, 1.0]
        self.light_color = [1.0, 1.0, 1.0, 1.0]
        self.light_ambient = [0.3, 0.3, 0.3, 1.0]
        self.light_intensity = 1.0
        self.light_type = 'directional'
        self.transform_matrix = np.eye(4)
        self.validation_messages = []
        self.show_lighting = True
        
    def show_message(self, title, message, msg_type="info"):
        root = Tk()
        root.withdraw()
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
        root.destroy()
        
    def add_point(self, x, y, z, name="", color=(1, 1, 1)):
        for p in self.points:
            if np.allclose(p.pos, [x, y, z], atol=0.001):
                self.show_message("Punct duplicat", 
                    f"Punct duplicat detectat la coordonatele:\n({x:.3f}, {y:.3f}, {z:.3f})\n\nPunctul nu va fi adaugat.",
                    "warning")
                return None
        point = Point3D(x, y, z, name, color)
        self.points.append(point)
        return len(self.points) - 1
    
    def add_edge(self, p1_idx, p2_idx, color=(0.7, 0.7, 0.7)):
        if p1_idx < 0 or p1_idx >= len(self.points) or p2_idx < 0 or p2_idx >= len(self.points):
            self.show_message("Legatura invalida",
                f"Legatura invalida: indici {p1_idx} -> {p2_idx}\n\nIndicii trebuie sa fie intre 0 si {len(self.points)-1}.",
                "error")
            return False
        if p1_idx == p2_idx:
            self.show_message("Legatura invalida",
                f"Nu se poate crea o legatura catre acelasi punct!\n\nPunctul {p1_idx} nu poate fi conectat la sine.",
                "error")
            return False
        edge = Edge(p1_idx, p2_idx, color)
        self.edges.append(edge)
        return True
    
    def add_face(self, indices, color=(0.5, 0.5, 0.8)):
        face = Face(indices, color)
        self.faces.append(face)
    
    def build_tree_structure(self):
        if len(self.points) < 2:
            return
        
        adjacency = {i: [] for i in range(len(self.points))}
        for edge in self.edges:
            adjacency[edge.p1_idx].append(edge.p2_idx)
            adjacency[edge.p2_idx].append(edge.p1_idx)
        
        root = 0
        for i, neighbors in adjacency.items():
            if len(neighbors) == 1:
                root = i
                break
        
        visited = set()
        tree_edges = []
        
        def dfs(node, parent=-1):
            visited.add(node)
            for neighbor in adjacency[node]:
                if neighbor not in visited and neighbor != parent:
                    tree_edges.append((node, neighbor))
                    dfs(neighbor, node)
        
        dfs(root)
        
        if tree_edges:
            self.edges.clear()
            for p1, p2 in tree_edges:
                self.add_edge(p1, p2)
            
            msg = f"Structura arborescent construita!\n\n"
            msg += f"Radacina: Punct {root}\n"
            msg += f"Muchii in arbore: {len(tree_edges)}\n"
            msg += f"Adancime maxima: {self.get_tree_depth(root, adjacency)}"
            self.show_message("Arbore construit", msg, "info")
    
    def get_tree_depth(self, root, adjacency):
        def depth_dfs(node, parent, current_depth):
            max_depth = current_depth
            for neighbor in adjacency[node]:
                if neighbor != parent:
                    max_depth = max(max_depth, depth_dfs(neighbor, node, current_depth + 1))
            return max_depth
        
        return depth_dfs(root, -1, 0)
    
    def generate_surfaces(self):
        if len(self.edges) < 3:
            self.show_message("Insuficiente muchii", 
                "Trebuie sa existe cel putin 3 muchii pentru a genera suprafete!", 
                "warning")
            return
        
        adjacency = {i: [] for i in range(len(self.points))}
        for edge in self.edges:
            adjacency[edge.p1_idx].append(edge.p2_idx)
            adjacency[edge.p2_idx].append(edge.p1_idx)
        
        self.faces.clear()
        found_faces = []
        
        for start in range(len(self.points)):
            for second in adjacency[start]:
                if second <= start:
                    continue
                
                for third in adjacency[second]:
                    if third <= start:
                        continue
                    if third in adjacency[start]:
                        face = tuple(sorted([start, second, third]))
                        if face not in found_faces:
                            found_faces.append(face)
                            self.add_face(list(face), self.generate_face_color(len(found_faces)))
        
        for start in range(len(self.points)):
            for second in adjacency[start]:
                if second <= start:
                    continue
                for third in adjacency[second]:
                    if third <= start or third == start:
                        continue
                    for fourth in adjacency[third]:
                        if fourth == start and fourth in adjacency[second]:
                            face = tuple(sorted([start, second, third, fourth]))
                            if face not in found_faces and len(face) == 4:
                                found_faces.append(face)
                                self.add_face(list(face), self.generate_face_color(len(found_faces)))
        
        msg = f"Suprafete generate automat!\n\n"
        msg += f"Triunghiuri si patrulatere gasite: {len(self.faces)}\n"
        msg += f"Din {len(self.edges)} muchii\n\n"
        if len(self.faces) == 0:
            msg += "Hint: Conecteaza punctele pentru a forma poligoane inchise!"
        
        self.show_message("Generare suprafete", msg, "info")
    
    def generate_face_color(self, index):
        colors = [
            (0.8, 0.3, 0.3), (0.3, 0.8, 0.3), (0.3, 0.3, 0.8),
            (0.8, 0.8, 0.3), (0.8, 0.3, 0.8), (0.3, 0.8, 0.8),
            (0.9, 0.5, 0.2), (0.5, 0.2, 0.9), (0.2, 0.9, 0.5)
        ]
        return colors[index % len(colors)]
    
    def generate_convex_hull(self):
        if len(self.points) < 4:
            self.show_message("Insuficiente puncte", 
                "Trebuie sa existe cel putin 4 puncte pentru convex hull!", 
                "warning")
            return
        
        from scipy.spatial import ConvexHull
        
        try:
            points_array = np.array([p.pos for p in self.points])
            hull = ConvexHull(points_array)
            
            self.faces.clear()
            for simplex in hull.simplices:
                self.add_face(list(simplex), self.generate_face_color(len(self.faces)))
            
            msg = f"Convex Hull generat!\n\n"
            msg += f"Fete create: {len(hull.simplices)}\n"
            msg += f"Puncte pe suprafata: {len(hull.vertices)}\n"
            msg += f"Volum: {hull.volume:.3f}\n"
            msg += f"Aria: {hull.area:.3f}"
            
            self.show_message("Convex Hull", msg, "info")
        except Exception as e:
            self.show_message("Eroare", 
                f"Nu s-a putut genera convex hull!\n\nPunctele trebuie sa fie 3D si non-coplanare.\n\nEroare: {str(e)}", 
                "error")
    
    def triangulate_faces(self):
        if not self.faces:
            self.show_message("Fara fete", "Nu exista fete de triangulat!", "warning")
            return
        
        new_faces = []
        for face in self.faces:
            if len(face.indices) == 3:
                new_faces.append(face)
            elif len(face.indices) > 3:
                for i in range(1, len(face.indices) - 1):
                    new_faces.append(Face([face.indices[0], face.indices[i], face.indices[i+1]], face.color))
        
        old_count = len(self.faces)
        self.faces = new_faces
        
        msg = f"Triangulare completa!\n\n"
        msg += f"Fete originale: {old_count}\n"
        msg += f"Triunghiuri rezultate: {len(self.faces)}"
        
        self.show_message("Triangulare", msg, "info")
    
    def auto_connect_tree(self):
        if len(self.points) < 2:
            return
        
        self.edges.clear()
        
        y_sorted = sorted(enumerate(self.points), key=lambda x: x[1].pos[1])
        trunk_base = y_sorted[0][0]
        
        connected = {trunk_base}
        unconnected = set(range(len(self.points))) - connected
        
        while unconnected:
            best_pair = None
            best_dist = float('inf')
            
            for conn in connected:
                for unconn in unconnected:
                    dist = np.linalg.norm(self.points[conn].pos - self.points[unconn].pos)
                    if dist < best_dist:
                        best_dist = dist
                        best_pair = (conn, unconn)
            
            if best_pair:
                self.add_edge(best_pair[0], best_pair[1])
                connected.add(best_pair[1])
                unconnected.remove(best_pair[1])
        
        msg = f"Arbore conectat automat!\n\n"
        msg += f"Radacina (cel mai jos punct): {trunk_base}\n"
        msg += f"Muchii create: {len(self.edges)}\n"
        msg += f"Puncte conectate: {len(self.points)}"
        self.show_message("Auto-conectare arbore", msg, "info")
    
    def load_sdl(self, filename):
        if not os.path.exists(filename):
            self.show_message("Eroare", f"Fisierul {filename} nu exista!", "error")
            return False
            
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            self.points.clear()
            self.edges.clear()
            self.faces.clear()
            self.validation_messages = []
            
            point_map = {}
            duplicates = 0
            invalid_edges = 0
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) < 4:
                    continue
                
                cmd = parts[0].upper()
                
                if cmd == 'V':
                    name = parts[1]
                    x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                    idx = self.add_point(x, y, z, name)
                    if idx is not None:
                        point_map[name] = idx
                    else:
                        duplicates += 1
                
                elif cmd == 'E':
                    if len(parts) >= 3:
                        p1_name, p2_name = parts[1], parts[2]
                        if p1_name in point_map and p2_name in point_map:
                            if not self.add_edge(point_map[p1_name], point_map[p2_name]):
                                invalid_edges += 1
                        else:
                            invalid_edges += 1
                            self.validation_messages.append(f"Muchie ignorata: {p1_name}->{p2_name} (punct inexistent)")
                
                elif cmd == 'F':
                    if len(parts) >= 4:
                        indices = [point_map[parts[i]] for i in range(1, len(parts)) if parts[i] in point_map]
                        if len(indices) >= 3:
                            self.add_face(indices)
            
            summary = f"SDL incarcat cu succes!\n\n"
            summary += f"Puncte create: {len(self.points)}\n"
            summary += f"Muchii create: {len(self.edges)}\n"
            summary += f"Fete create: {len(self.faces)}\n"
            
            if duplicates > 0 or invalid_edges > 0:
                summary += f"\n--- VALIDARI ---\n"
                if duplicates > 0:
                    summary += f"Puncte duplicate ignorate: {duplicates}\n"
                if invalid_edges > 0:
                    summary += f"Muchii invalide ignorate: {invalid_edges}\n"
                
            self.show_message("Incarcare SDL", summary, "info")
            return True
            
        except Exception as e:
            self.show_message("Eroare", f"Eroare la incarcarea SDL:\n{str(e)}", "error")
            return False
    
    def export_sdl(self, filename):
        try:
            with open(filename, 'w') as f:
                f.write("# SDL Export\n")
                
                for i, p in enumerate(self.points):
                    name = p.name if p.name else f"V{i}"
                    f.write(f"V {name} {p.pos[0]:.4f} {p.pos[1]:.4f} {p.pos[2]:.4f}\n")
                
                for e in self.edges:
                    name1 = self.points[e.p1_idx].name if self.points[e.p1_idx].name else f"V{e.p1_idx}"
                    name2 = self.points[e.p2_idx].name if self.points[e.p2_idx].name else f"V{e.p2_idx}"
                    f.write(f"E {name1} {name2}\n")
                
                for face in self.faces:
                    names = [self.points[i].name if self.points[i].name else f"V{i}" for i in face.indices]
                    f.write(f"F {' '.join(names)}\n")
            
            self.show_message("Export SDL", f"Fisier exportat cu succes!\n\nLocatie: {filename}", "info")
            return True
        except Exception as e:
            self.show_message("Eroare export", f"Eroare la exportul SDL:\n{str(e)}", "error")
            return False
    
    def export_json(self, filename):
        try:
            data = {
                'points': [{'x': p.pos[0], 'y': p.pos[1], 'z': p.pos[2], 
                           'name': p.name, 'color': p.color} for p in self.points],
                'edges': [{'p1': e.p1_idx, 'p2': e.p2_idx, 'color': e.color} for e in self.edges],
                'faces': [{'indices': f.indices, 'color': f.color} for f in self.faces],
                'camera': {'distance': self.camera.distance, 'yaw': self.camera.yaw, 'pitch': self.camera.pitch}
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.show_message("Export JSON", f"Fisier exportat cu succes!\n\nLocatie: {filename}", "info")
        except Exception as e:
            self.show_message("Eroare export", f"Eroare la exportul JSON:\n{str(e)}", "error")
    
    def create_cube_example(self):
        self.points.clear()
        self.edges.clear()
        self.faces.clear()
        
        cube_verts = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ]
        
        edge_midpoints = [
            [0, -1, -1], [1, 0, -1], [0, 1, -1], [-1, 0, -1],
            [0, -1, 1], [1, 0, 1], [0, 1, 1], [-1, 0, 1],
            [-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]
        ]
        
        face_centers = [
            [0, 0, -1], [0, 0, 1], [0, -1, 0], [0, 1, 0], [-1, 0, 0], [1, 0, 0]
        ]
        
        all_points = cube_verts + edge_midpoints + face_centers
        
        for i, p in enumerate(all_points):
            self.add_point(p[0], p[1], p[2], f"P{i}", (0.3 + i*0.02, 0.5, 0.7))
        
        cube_edges = [
            (0,1), (1,2), (2,3), (3,0),
            (4,5), (5,6), (6,7), (7,4),
            (0,4), (1,5), (2,6), (3,7)
        ]
        for e in cube_edges:
            self.add_edge(e[0], e[1])
        
        self.add_face([0, 1, 2, 3], (0.8, 0.3, 0.3))
        self.add_face([4, 5, 6, 7], (0.3, 0.8, 0.3))
        self.add_face([0, 1, 5, 4], (0.3, 0.3, 0.8))
        self.add_face([2, 3, 7, 6], (0.8, 0.8, 0.3))
    
    def get_centroid(self):
        if not self.points:
            return np.array([0, 0, 0])
        return np.mean([p.pos for p in self.points], axis=0)
    
    def get_bounding_box(self):
        if not self.points:
            return None
        points = np.array([p.pos for p in self.points])
        return np.min(points, axis=0), np.max(points, axis=0)
    
    def get_edge_length(self, edge_idx):
        if edge_idx < 0 or edge_idx >= len(self.edges):
            return 0
        e = self.edges[edge_idx]
        p1 = self.points[e.p1_idx].pos
        p2 = self.points[e.p2_idx].pos
        return np.linalg.norm(p2 - p1)
    
    def translate(self, dx, dy, dz):
        for p in self.points:
            p.pos += np.array([dx, dy, dz])
    
    def rotate(self, axis, angle_deg):
        angle = math.radians(angle_deg)
        centroid = self.get_centroid()
        
        if axis == 'x':
            rot = np.array([[1, 0, 0],
                           [0, math.cos(angle), -math.sin(angle)],
                           [0, math.sin(angle), math.cos(angle)]])
        elif axis == 'y':
            rot = np.array([[math.cos(angle), 0, math.sin(angle)],
                           [0, 1, 0],
                           [-math.sin(angle), 0, math.cos(angle)]])
        else:
            rot = np.array([[math.cos(angle), -math.sin(angle), 0],
                           [math.sin(angle), math.cos(angle), 0],
                           [0, 0, 1]])
        
        for p in self.points:
            p.pos = centroid + rot @ (p.pos - centroid)
    
    def scale(self, factor):
        centroid = self.get_centroid()
        for p in self.points:
            p.pos = centroid + (p.pos - centroid) * factor
    
    def mirror(self, axis):
        axis_idx = {'x': 0, 'y': 1, 'z': 2}[axis]
        centroid = self.get_centroid()
        for p in self.points:
            relative = p.pos - centroid
            relative[axis_idx] *= -1
            p.pos = centroid + relative
    
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.apply()
        
        if self.show_lighting:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            
            if self.light_type == 'directional':
                light_pos = [self.light_position[0], self.light_position[1], self.light_position[2], 0.0]
            else:
                light_pos = [self.light_position[0], self.light_position[1], self.light_position[2], 1.0]
            
            glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
            
            diffuse = [c * self.light_intensity for c in self.light_color[:3]] + [1.0]
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
            glLightfv(GL_LIGHT0, GL_AMBIENT, self.light_ambient)
            glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 32.0)
        
        if self.render_mode == 'solid' and self.faces:
            glEnable(GL_LIGHTING) if self.show_lighting else glDisable(GL_LIGHTING)
            for face in self.faces:
                glBegin(GL_POLYGON)
                glColor3f(*face.color)
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, face.color + (1.0,))
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [c * 0.3 for c in face.color] + [1.0])
                
                if len(face.indices) >= 3:
                    p0 = self.points[face.indices[0]].pos
                    p1 = self.points[face.indices[1]].pos
                    p2 = self.points[face.indices[2]].pos
                    v1 = p1 - p0
                    v2 = p2 - p0
                    normal = np.cross(v1, v2)
                    norm = np.linalg.norm(normal)
                    if norm > 0:
                        normal /= norm
                    glNormal3f(*normal)
                
                for idx in face.indices:
                    glVertex3f(*self.points[idx].pos)
                glEnd()
        
        glDisable(GL_LIGHTING)
        
        if self.render_mode in ['wireframe', 'solid']:
            glLineWidth(2.0)
            glBegin(GL_LINES)
            for edge in self.edges:
                glColor3f(*edge.color)
                glVertex3f(*self.points[edge.p1_idx].pos)
                glVertex3f(*self.points[edge.p2_idx].pos)
            glEnd()
        
        glPointSize(8.0)
        glBegin(GL_POINTS)
        for p in self.points:
            if p.selected:
                glColor3f(1.0, 1.0, 0.0)
            else:
                glColor3f(*p.color)
            glVertex3f(*p.pos)
        glEnd()
        
        self.render_axes()
        
        if self.show_lighting:
            self.render_light_indicator()
    
    def render_axes(self):
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(2, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 2, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 2)
        glEnd()
    
    def render_light_indicator(self):
        glDisable(GL_LIGHTING)
        glPointSize(15.0)
        glBegin(GL_POINTS)
        glColor3f(*self.light_color[:3])
        glVertex3f(self.light_position[0], self.light_position[1], self.light_position[2])
        glEnd()
        
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glColor3f(1, 1, 0)
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if i == 0 and j == 0 and k == 0:
                        continue
                    glVertex3f(self.light_position[0], self.light_position[1], self.light_position[2])
                    glVertex3f(self.light_position[0] + i*0.3, 
                              self.light_position[1] + j*0.3, 
                              self.light_position[2] + k*0.3)
        glEnd()

class Application:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Editor 3D SDL - Proiect Final")
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glClearColor(0.1, 0.1, 0.15, 1.0)
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        
        self.scene = Scene3D()
        self.scene.create_cube_example()
        
        self.mouse_down = False
        self.last_mouse_pos = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.show_info = True
        
        self.input_mode = False
        self.input_text = ""
        self.input_step = 0
        self.temp_coords = [0.0, 0.0, 0.0]
        self.first_point_for_edge = None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.input_mode:
                    if event.button == 1:
                        clicked_point = self.get_clicked_point(event.pos)
                        if clicked_point is not None:
                            self.scene.selected_point = clicked_point
                            for i, p in enumerate(self.scene.points):
                                p.selected = (i == clicked_point)
                        else:
                            self.mouse_down = True
                            self.last_mouse_pos = pygame.mouse.get_pos()
                    elif event.button == 4:
                        self.scene.camera.distance = max(2, self.scene.camera.distance - 0.5)
                    elif event.button == 5:
                        self.scene.camera.distance = min(50, self.scene.camera.distance + 0.5)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_down and self.last_mouse_pos and not self.input_mode:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.scene.camera.yaw += dx * 0.5
                    self.scene.camera.pitch = max(-89, min(89, self.scene.camera.pitch - dy * 0.5))
                    self.last_mouse_pos = event.pos
            
            elif event.type == pygame.KEYDOWN:
                if self.input_mode:
                    self.handle_input_keypress(event)
                else:
                    self.handle_keypress(event.key)
    
    def get_clicked_point(self, mouse_pos):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        threshold = 15
        
        for i, point in enumerate(self.scene.points):
            try:
                win_coords = gluProject(
                    point.pos[0], point.pos[1], point.pos[2],
                    modelview, projection, viewport
                )
                
                screen_x = win_coords[0]
                screen_y = viewport[3] - win_coords[1]
                
                dx = mouse_pos[0] - screen_x
                dy = mouse_pos[1] - screen_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < threshold:
                    return i
            except:
                continue
        
        return None
    
    def handle_keypress(self, key):
        if key == pygame.K_t:
            self.input_mode = True
            self.input_step = 0
            self.input_text = ""
            self.temp_coords = [0.0, 0.0, 0.0]
            print("\n=== INTRODUCERE PUNCT MANUAL ===")
            print("Introdu coordonata X (apoi ENTER):")
            return
        
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            if self.scene.selected_point is not None:
                idx = self.scene.selected_point
                if 0 <= idx < len(self.scene.points):
                    self.scene.edges = [e for e in self.scene.edges 
                                       if e.p1_idx != idx and e.p2_idx != idx]
                    del self.scene.points[idx]
                    for e in self.scene.edges:
                        if e.p1_idx > idx:
                            e.p1_idx -= 1
                        if e.p2_idx > idx:
                            e.p2_idx -= 1
                    self.scene.selected_point = None
                    self.scene.show_message("Punct sters", 
                        f"Punctul a fost sters cu succes!\n\nPuncte ramase: {len(self.scene.points)}", 
                        "info")
            return
        
        elif key == pygame.K_TAB:
            if self.scene.points:
                if self.scene.selected_point is None:
                    self.scene.selected_point = 0
                else:
                    self.scene.selected_point = (self.scene.selected_point + 1) % len(self.scene.points)
                for i, p in enumerate(self.scene.points):
                    p.selected = (i == self.scene.selected_point)
            return
        
        elif key == pygame.K_c:
            if self.scene.selected_point is not None:
                if self.first_point_for_edge is None:
                    self.first_point_for_edge = self.scene.selected_point
                    self.scene.show_message("Conectare puncte", 
                        f"Primul punct selectat: {self.first_point_for_edge}\n\nSelecteaza al doilea punct cu TAB si apasa C din nou.", 
                        "info")
                else:
                    if self.scene.add_edge(self.first_point_for_edge, self.scene.selected_point):
                        self.scene.show_message("Muchie adaugata", 
                            f"Muchie creata cu succes!\n\n{self.first_point_for_edge} -> {self.scene.selected_point}\n\nTotal muchii: {len(self.scene.edges)}", 
                            "info")
                    self.first_point_for_edge = None
            return
        
        if key == pygame.K_w:
            self.scene.translate(0, 0.2, 0)
        elif key == pygame.K_s:
            self.scene.translate(0, -0.2, 0)
        elif key == pygame.K_a:
            self.scene.translate(-0.2, 0, 0)
        elif key == pygame.K_d:
            self.scene.translate(0.2, 0, 0)
        elif key == pygame.K_q:
            self.scene.translate(0, 0, -0.2)
        elif key == pygame.K_e:
            self.scene.translate(0, 0, 0.2)
        
        elif key == pygame.K_x:
            self.scene.rotate('x', 15)
        elif key == pygame.K_y:
            self.scene.rotate('y', 15)
        elif key == pygame.K_z:
            self.scene.rotate('z', 15)
        
        elif key == pygame.K_EQUALS or key == pygame.K_PLUS:
            self.scene.scale(1.1)
        elif key == pygame.K_MINUS:
            self.scene.scale(0.9)
        
        elif key == pygame.K_1:
            self.scene.mirror('x')
        elif key == pygame.K_2:
            self.scene.mirror('y')
        elif key == pygame.K_3:
            self.scene.mirror('z')
        
        elif key == pygame.K_m:
            modes = ['wireframe', 'solid', 'points']
            current_idx = modes.index(self.scene.render_mode)
            self.scene.render_mode = modes[(current_idx + 1) % 3]
        elif key == pygame.K_v:
            self.scene.render_mode = 'wireframe'
        elif key == pygame.K_b:
            self.scene.render_mode = 'solid'
        elif key == pygame.K_n:
            self.scene.render_mode = 'points'
        
        elif key == pygame.K_i:
            self.show_info = not self.show_info
        
        elif key == pygame.K_o:
            self.scene.export_sdl("output.sdl")
        elif key == pygame.K_p:
            self.scene.export_json("output.json")
        
        elif key == pygame.K_l:
            root = Tk()
            root.withdraw()
            filename = filedialog.askopenfilename(
                title="Selecteaza fisier SDL",
                filetypes=[("SDL files", "*.sdl"), ("All files", "*.*")]
            )
            root.destroy()
            if filename:
                self.scene.load_sdl(filename)
        
        elif key == pygame.K_r:
            self.scene.create_cube_example()
        
        elif key == pygame.K_g:
            self.print_geometry_info()
        
        elif key == pygame.K_u:
            self.scene.auto_connect_tree()
        
        elif key == pygame.K_j:
            self.scene.build_tree_structure()
        
        elif key == pygame.K_f:
            self.scene.generate_surfaces()
        
        elif key == pygame.K_h:
            try:
                self.scene.generate_convex_hull()
            except ImportError:
                self.scene.show_message("Scipy necesar", 
                    "Pentru Convex Hull trebuie instalat scipy:\n\npip install scipy", 
                    "warning")
        
        elif key == pygame.K_k:
            self.scene.triangulate_faces()
        
        elif key == pygame.K_9:
            self.scene.light_type = 'directional' if self.scene.light_type == 'point' else 'point'
            self.scene.show_message("Tip lumina", 
                f"Tip lumina: {self.scene.light_type.upper()}", "info")
        
        elif key == pygame.K_0:
            self.scene.show_lighting = not self.scene.show_lighting
            status = "ACTIVATA" if self.scene.show_lighting else "DEZACTIVATA"
            self.scene.show_message("Iluminare", f"Iluminare: {status}", "info")
        
        elif key == pygame.K_UP:
            self.scene.light_intensity = min(2.0, self.scene.light_intensity + 0.1)
        elif key == pygame.K_DOWN:
            self.scene.light_intensity = max(0.1, self.scene.light_intensity - 0.1)
        
        elif key == pygame.K_LEFT:
            self.scene.light_position[0] -= 0.5
        elif key == pygame.K_RIGHT:
            self.scene.light_position[0] += 0.5
        elif key == pygame.K_PAGEUP:
            self.scene.light_position[1] += 0.5
        elif key == pygame.K_PAGEDOWN:
            self.scene.light_position[1] -= 0.5
        
        elif key == pygame.K_8:
            colors = [(1,1,1), (1,0.8,0.6), (0.6,0.8,1), (1,0.6,0.6), (0.6,1,0.6)]
            names = ["Alb", "Cald", "Rece", "Rosu", "Verde"]
            current = self.scene.light_color[:3]
            try:
                idx = colors.index(tuple(current))
                idx = (idx + 1) % len(colors)
            except:
                idx = 0
            self.scene.light_color = list(colors[idx]) + [1.0]
            self.scene.show_message("Culoare lumina", f"Culoare: {names[idx]}", "info")
    
    def handle_input_keypress(self, event):
        if event.key == pygame.K_RETURN:
            try:
                value = float(self.input_text)
                self.temp_coords[self.input_step] = value
                
                self.input_step += 1
                self.input_text = ""
                
                if self.input_step == 3:
                    idx = self.scene.add_point(
                        self.temp_coords[0],
                        self.temp_coords[1],
                        self.temp_coords[2],
                        f"P{len(self.scene.points)}",
                        (0.2 + len(self.scene.points) * 0.03, 0.8, 0.3)
                    )
                    if idx is not None:
                        self.scene.show_message("Punct adaugat", 
                            f"Punct creat cu succes!\n\nCoordonare: ({self.temp_coords[0]:.3f}, {self.temp_coords[1]:.3f}, {self.temp_coords[2]:.3f})\n\nTotal puncte: {len(self.scene.points)}", 
                            "info")
                    
                    self.input_mode = False
                    self.input_step = 0
                    self.input_text = ""
                    
            except ValueError:
                self.scene.show_message("Valoare invalida", "Te rog introdu un numar valid!", "error")
                self.input_text = ""
        
        elif event.key == pygame.K_ESCAPE:
            self.input_mode = False
            self.input_step = 0
            self.input_text = ""
        
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        
        elif event.key == pygame.K_MINUS:
            self.input_text += "-"
        
        elif event.unicode.isdigit() or event.unicode == '.':
            self.input_text += event.unicode
    
    def print_geometry_info(self):
        info = "=== ANALIZA GEOMETRICA ===\n\n"
        info += f"Numar puncte: {len(self.scene.points)}\n"
        info += f"Numar muchii: {len(self.scene.edges)}\n"
        info += f"Numar fete: {len(self.scene.faces)}\n\n"
        
        centroid = self.scene.get_centroid()
        info += f"Centroid:\n({centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f})\n\n"
        
        bbox = self.scene.get_bounding_box()
        if bbox:
            info += f"Bounding Box:\n"
            info += f"Min: ({bbox[0][0]:.3f}, {bbox[0][1]:.3f}, {bbox[0][2]:.3f})\n"
            info += f"Max: ({bbox[1][0]:.3f}, {bbox[1][1]:.3f}, {bbox[1][2]:.3f})\n\n"
            size = bbox[1] - bbox[0]
            info += f"Dimensiuni:\n{size[0]:.3f} x {size[1]:.3f} x {size[2]:.3f}\n\n"
        
        if self.scene.edges:
            lengths = [self.scene.get_edge_length(i) for i in range(len(self.scene.edges))]
            info += f"Lungime muchie medie: {np.mean(lengths):.3f}\n"
            info += f"Lungime muchie min/max:\n{min(lengths):.3f} / {max(lengths):.3f}"
        
        self.scene.show_message("Analiza Geometrica", info, "info")
    
    def render_ui(self):
        if not self.show_info:
            return
        
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0, 0, 0, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(5, 5)
        glVertex2f(480, 5)
        glVertex2f(480, 280)
        glVertex2f(5, 280)
        glEnd()
        
        font = pygame.font.Font(None, 20)
        
        info_lines = [
            "=== EDITOR 3D SDL ===",
            f"Puncte: {len(self.scene.points)} | Muchii: {len(self.scene.edges)} | Fete: {len(self.scene.faces)}",
            f"Mod: {self.scene.render_mode.upper()} | Lumina: {self.scene.light_type.upper()} {'ON' if self.scene.show_lighting else 'OFF'}",
            f"Intensitate: {self.scene.light_intensity:.1f} | Culoare: RGB({self.scene.light_color[0]:.1f},{self.scene.light_color[1]:.1f},{self.scene.light_color[2]:.1f})",
            "",
            "EDIT: T-Add | CLICK-Select | DEL-Delete | C-Connect",
            "TREE: U-Auto | J-Build | SURFACE: F-Gen | H-Hull | K-Triangulate",
            "MOVE: WASD/QE | ROTATE: XYZ | SCALE: +/- | MIRROR: 1/2/3",
            "LIGHT: 9-Type | 0-On/Off | 8-Color | Arrows-Move | UP/DN-Intensity",
            "VIEW: M-Mode | VBN-Wire/Solid/Pts | G-Info | I-UI | R-Reset | L-Load"
        ]
        
        if self.input_mode:
            coord_names = ['X', 'Y', 'Z']
            info_lines.append("")
            info_lines.append(f">>> INTRODUCERE COORDONATA {coord_names[self.input_step]}: {self.input_text}_")
            info_lines.append("ENTER - Confirma | ESC - Anuleaza")
        
        y_offset = 15
        for line in info_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_data = pygame.image.tostring(text_surface, "RGBA", True)
            w, h = text_surface.get_size()
            
            glRasterPos2f(10, y_offset)
            glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            y_offset += 25
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopAttrib()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.scene.render()
            self.render_ui()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    app = Application()
    app.run()
