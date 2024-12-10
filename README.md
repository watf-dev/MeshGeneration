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
```
./run_2d.sh 40 10
```
- arg 1: the number of elements in x
- arg 2: the number of elements in y

## Visualization with ParaView
Example mesh with 40 elements in x and 10 elements in y;
![Example 2D Mesh](figs/pic_2d.png)
![Example 3D Mesh](figs/pic_3d.png)

