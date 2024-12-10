# Mesh Generation
A personal project to show my academic output and skillset.

## Cloning the Repository
To clone the repository,
```
git clone https://github.com/watf-dev/MeshGeneration.git
```

## Setting required modules
- [watfmesh](https://github.com/watf-dev/watfmesh)

- [watf.nurbs](https://github.com/watf-dev/watf/tree/main/nurbs)

To add the directory to the PATH, for example,
```
echo 'export PATH=$PATH:/path/to/directory' >> ~/.zshrc
source ~/.zshrc
```

## Run
for 2D,
```
./run.sh 40 10
```
for 3D,
```
./run.sh 10 10 10
```
- arg 1: the number of elements in x
- arg 2: the number of elements in y
- arg 3: the number of elements in z

## Visualization with ParaView
Example 2D mesh with 40 elements in x and 10 elements in y;
![Example 2D Mesh](figs/pic_2d.png)
Example 3D mesh with 10 elements in all directions;
![Example 3D Mesh](figs/pic_3d.png)

