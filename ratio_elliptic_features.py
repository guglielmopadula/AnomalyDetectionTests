import meshio
import numpy as np
from sklearn.covariance import EllipticEnvelope
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.manifold import Isomap
points=meshio.read("data/Stanford_Bunny_red.stl").points
triangles=meshio.read("data/Stanford_Bunny_red.stl").cells_dict['triangle']

all_points=np.zeros((600,len(points),3))

all_points_out=np.zeros((20,len(points),3))
for i in range(600):
    all_points[i]=meshio.read("data/bunny_coarse_train_"+str(i)+".ply").points


for k in range(20):
    all_points_out[k]=meshio.read("data/bunny_coarse_train_out_"+str(k)+".ply").points


labels=np.ones(600,dtype=np.int64)
labels_out=-np.ones(20,dtype=np.int64)
labels_train=labels[:500]
labels_test=labels[500:]
labels_out_train=labels_out[:10]
labels_out_test=labels_out[10:]
labels_all_train=np.concatenate((labels_train,labels_out_train))
labels_all_test=np.concatenate((labels_test,labels_out_test))
all_points_train=np.concatenate((all_points[:500],all_points_out[:10]))
all_points_test=np.concatenate((all_points[500:],all_points_out[10:]))
train_index=np.random.permutation(510)
test_index=np.random.permutation(110)
all_points_train=all_points_train[train_index]
all_points_test=all_points_test[test_index]
labels_all_train=labels_all_train[train_index]
labels_all_test=labels_all_test[test_index]
all_points_train_tri=all_points_train[:,triangles,:]
all_points_test_tri=all_points_test[:,triangles,:]

angles_0=np.arccos(np.sum((all_points_train_tri[:,:,2,:]-all_points_train_tri[:,:,0,:])*(all_points_train_tri[:,:,1,:]-all_points_train_tri[:,:,0,:]),axis=-1)/(np.linalg.norm(all_points_train_tri[:,:,2,:]-all_points_train_tri[:,:,0,:],axis=-1)*np.linalg.norm(all_points_train_tri[:,:,1,:]-all_points_train_tri[:,:,0,:],axis=-1)))
angles_1=np.arccos(np.sum((all_points_train_tri[:,:,0,:]-all_points_train_tri[:,:,1,:])*(all_points_train_tri[:,:,2,:]-all_points_train_tri[:,:,1,:]),axis=-1)/(np.linalg.norm(all_points_train_tri[:,:,0,:]-all_points_train_tri[:,:,1,:],axis=-1)*np.linalg.norm(all_points_train_tri[:,:,2,:]-all_points_train_tri[:,:,1,:],axis=-1)))
angles_2=np.arccos(np.sum((all_points_train_tri[:,:,1,:]-all_points_train_tri[:,:,2,:])*(all_points_train_tri[:,:,0,:]-all_points_train_tri[:,:,2,:]),axis=-1)/(np.linalg.norm(all_points_train_tri[:,:,1,:]-all_points_train_tri[:,:,2,:],axis=-1)*np.linalg.norm(all_points_train_tri[:,:,0,:]-all_points_train_tri[:,:,2,:],axis=-1)))

reg_train=np.abs(4*np.sin(angles_0/2)*np.sin(angles_1/2)*np.sin(angles_2/2))
angles_0=np.arccos(np.sum((all_points_test_tri[:,:,2,:]-all_points_test_tri[:,:,0,:])*(all_points_test_tri[:,:,1,:]-all_points_test_tri[:,:,0,:]),axis=-1)/(np.linalg.norm(all_points_test_tri[:,:,2,:]-all_points_test_tri[:,:,0,:],axis=-1)*np.linalg.norm(all_points_test_tri[:,:,1,:]-all_points_test_tri[:,:,0,:],axis=-1)))
angles_1=np.arccos(np.sum((all_points_test_tri[:,:,0,:]-all_points_test_tri[:,:,1,:])*(all_points_test_tri[:,:,2,:]-all_points_test_tri[:,:,1,:]),axis=-1)/(np.linalg.norm(all_points_test_tri[:,:,0,:]-all_points_test_tri[:,:,1,:],axis=-1)*np.linalg.norm(all_points_test_tri[:,:,2,:]-all_points_test_tri[:,:,1,:],axis=-1)))
angles_2=np.arccos(np.sum((all_points_test_tri[:,:,1,:]-all_points_test_tri[:,:,2,:])*(all_points_test_tri[:,:,0,:]-all_points_test_tri[:,:,2,:]),axis=-1)/(np.linalg.norm(all_points_test_tri[:,:,1,:]-all_points_test_tri[:,:,2,:],axis=-1)*np.linalg.norm(all_points_test_tri[:,:,0,:]-all_points_test_tri[:,:,2,:],axis=-1)))

                         
reg_test=4*np.sin(angles_0/2)*np.sin(angles_1/2)*np.sin(angles_2/2)



isomap=Isomap(n_neighbors=10,n_components=2)
isomap.fit(reg_train)   

clf =  EllipticEnvelope(contamination=0.02)
clf.fit(isomap.transform(reg_train).reshape(510,-1))
labels_all_train_pred=clf.predict(isomap.transform(reg_train).reshape(510,-1))
print(labels_all_train_pred)
labels_all_test_pred=clf.predict(isomap.transform(reg_test).reshape(110,-1))
print(labels_all_train_pred)
print(labels_all_test_pred)

auc_train = metrics.roc_auc_score((labels_all_train+1)//2, (labels_all_train_pred+1)//2)
auc_test = metrics.roc_auc_score((labels_all_test+1)//2, (labels_all_test_pred+1)//2)

print("AUC train: ",auc_train)
print("AUC test: ",auc_test)

