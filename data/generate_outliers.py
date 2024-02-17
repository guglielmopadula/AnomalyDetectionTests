import meshio
import numpy as np
points=meshio.read("data/Stanford_Bunny_red.stl").points
triangles=meshio.read("data/Stanford_Bunny_red.stl").cells_dict['triangle']

all_points=np.zeros((600,len(points),3))

all_points_out=np.zeros((20,len(points),3))
for i in range(600):
    all_points[i]=meshio.read("data/bunny_coarse_train_"+str(i)+".ply").points


for k in range(20):
    i=np.random.randint(600)
    j=np.random.randint(len(all_points))
    all_points_out[k]=all_points[i]
    all_points_out[k,j]+=2*np.random.rand(3)
    meshio.write_points_cells("data/bunny_coarse_train_out_"+str(k)+".ply",all_points_out[k],{"triangle":triangles})

    
