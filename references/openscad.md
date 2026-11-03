# OpenSCAD Scripting & Headless Export Reference

*Programmatic Constructive Solid Geometry (CSG) modeling engine.*

---

## 1. Parametric Modeling Syntax

OpenSCAD models objects by combining geometric primitives with boolean operators (`union`, `difference`, `intersection`):

```scad
// --- Parametric Enclosure Script (enclosure.scad) ---
$fn = 60; // Curve facet resolution

// User customizable parameters
pcb_length = 85.0;
pcb_width  = 56.0;
pcb_height = 1.6;
wall       = 2.0;
clearance  = 0.4;
box_height = 25.0;

outer_l = pcb_length + 2 * (wall + clearance);
outer_w = pcb_width  + 2 * (wall + clearance);

module rounded_box(l, w, h, r) {
    hull() {
        translate([r, r, 0]) cylinder(h=h, r=r);
        translate([l-r, r, 0]) cylinder(h=h, r=r);
        translate([r, w-r, 0]) cylinder(h=h, r=r);
        translate([l-r, w-r, 0]) cylinder(h=h, r=r);
    }
}

module enclosure_bottom() {
    difference() {
        // Outer Body
        rounded_box(outer_l, outer_w, box_height, 3.0);
        
        // Inner Pocket Hollow
        translate([wall, wall, wall])
            rounded_box(outer_l - 2*wall, outer_w - 2*wall, box_height, 2.0);
            
        // USB-C Connector Cutout on side
        translate([-1, outer_w/2 - 5, wall + 3.0])
            cube([wall + 2, 10.0, 4.0]);
    }
    
    // Standoff Bosses
    boss_r = 2.0;
    boss_hole_r = 0.8; // M2 screw pilot hole
    standoff_h = 5.0;
    
    boss_coords = [
        [wall + clearance + 4, wall + clearance + 4],
        [outer_l - wall - clearance - 4, wall + clearance + 4],
        [wall + clearance + 4, outer_w - wall - clearance - 4],
        [outer_l - wall - clearance - 4, outer_w - wall - clearance - 4]
    ];
    
    for (pos = boss_coords) {
        translate([pos[0], pos[1], wall])
            difference() {
                cylinder(h=standoff_h, r=boss_r);
                translate([0,0,-0.1])
                    cylinder(h=standoff_h + 0.2, r=boss_hole_r);
            }
    }
}

enclosure_bottom();
```

---

## 2. Advanced 2D to 3D Extrusions

- **Linear Extrusion with Twist & Scale**:
  ```scad
  linear_extrude(height = 30, twist = 90, scale = 0.8, slices = 100)
      square([20, 20], center = true);
  ```
- **Rotational Extrusion (Lathe operations)**:
  ```scad
  rotate_extrude(angle = 360, $fn = 100)
      translate([20, 0, 0])
          circle(r = 5); // Torus O-ring seal
  ```
- **Minkowski Sum (Edge rounding / Softening)**:
  ```scad
  minkowski() {
      cube([50, 30, 10]);
      sphere(r = 2.0, $fn = 30);
  }
  ```

---

## 3. Headless CLI Rendering & Batch Export

Execute headless exports without launching the GUI:

```bash
# 1. Export STL for 3D Printing
openscad -o mech/enclosure.stl mech/enclosure.scad

# 2. Parameter Override on CLI (e.g. adjust width and wall thickness)
openscad -o mech/enclosure_wide.stl -D "pcb_length=100.0" -D "wall=2.5" mech/enclosure.scad

# 3. Export 3D Manufacturing Format (3MF)
openscad -o mech/enclosure.3mf mech/enclosure.scad

# 4. Export CSG Solid or DXF Projection
openscad -o mech/enclosure.csg mech/enclosure.scad
openscad -o mech/cutout.dxf -D "projection(cut = true) enclosure_bottom();" mech/enclosure.scad

# 5. Headless PNG Snapshot Rendering
openscad -o docs/enclosure_preview.png --imgsize=1920,1080 --camera=0,0,0,55,0,25,200 --colorscheme=Solarized mech/enclosure.scad
```
