import os
import hashlib
import numpy,scipy, os, array
import scipy.misc
import Image,leargist
from sklearn.cluster import MeanShift
from scipy.spatial.distance import pdist,squareform
import time
import pylab as plt

def banner(text, ch='=', length=78):
	spaced_text = ' %s ' % text
	banner = spaced_text.center(length,ch)
	return banner

print banner ('LITTLE MALWARE CLUSTERER ^_^');

dirname="XXXX" # the directory where malware samples reside

list= os.listdir(dirname);
length=len(list);
corpus_features= [ [ 0 for i in range(320) ] for j in range(length) ]
sample= [ 0 for i in range(length) ]
sample_name= [ 0 for i in range(length) ]


for y in range(0, length):
	x=dirname+'/'+list[y];
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(x,'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf=afile.read(BLOCKSIZE)
	hash=(hasher.hexdigest())
	filename = x;
	f = open(filename,'rb');
	ln = os.path.getsize(filename); # length of file in bytes
	width = 256;
	rem = ln%width; 
	a = array.array("B"); # uint8 array
	a.fromfile(f,ln-rem);
	f.close(); 
	g = numpy.reshape(a,(len(a)/width,width));
	g = numpy.uint8(g);
	scipy.misc.imsave('images/'+hash+'.png',g); # save the image
	im = Image.open('images/'+hash+'.png');
	im1 = im.resize((64,64)); # for faster computation
	des = leargist.color_gist(im1); # 960 values
	feature = des[0:320]; # since the image is grayscale, we need only first 320 values
	sample[y]=hash; 
	sample_name[y]=list[y];

	corpus_features[y]=feature;


print 'Done creating malware images';


numpy.save('corpus_features.npy',corpus_features); 

X = numpy.load('corpus_features.npy');

ms1 = MeanShift(bandwidth=0.2);
tic = time.time();
ms1.fit(X);
toc = time.time();
print "Done clustering";
print "Elasped Time (s) = ", toc-tic;


##visualize
labels1 = ms1.labels_;
labels1_u = numpy.unique(labels1);
l_sort_ind = numpy.argsort(labels1);

cluster_centers1= ms1.cluster_centers_;
n_clusters_ = len(labels1_u);
print ("number of clusters: %d" % n_clusters_)

chkdir= os.listdir("clustered");
print "Saving results..."	
if len(chkdir)!=0:
	os.system("rm -r clustered/*");
	print "Found Files .. too bad for them!!"	
	print "Directory cleaned";



for k in range(n_clusters_):
	my_members = labels1 == k

	
	arr= X[my_members,0];

	os.system("mkdir clustered/cluster_%d" % k);
	file = open("clustered/cluster_%d"%k+"/list_%d"%k, "w+");

	file.write ("cluster {0}: {1}".format(k, X[my_members,0]));
	for z in range(length):
		for zz in range(len(arr)):
			if arr[zz]==corpus_features[z][0]:
				file.write("\n");
				file.write ('filename: '+sample_name[z]);
				file.write("\n");
				file.write('sha1: '+sample[z]);


	
file.close();


X_sort = numpy.zeros((X.shape[0],X.shape[1]));
for i in range(X.shape[0]):
  X_sort[i] = X[l_sort_ind[i]];

yd_sort = pdist(X_sort,'euclidean');
yd_sort_sq = squareform(yd_sort);
yd_sort_sq.shape;

plt.imshow(yd_sort_sq/yd_sort_sq.max());
plt.colorbar();
plt.show();

print ("Thanks for having fun with me :) Bye.")
