import numpy as np
import matplotlib.pyplot as plt
def main():
    grayscale_image=np.random.randint(0,256,size=(200,300))
    color_image=np.stack([grayscale_image]*3,axis=2)
    #老大这里为什么最开始全是全角的啊喂
    #加滤镜
    sepia_matrix = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131]
    ]).T
    color_image=np.dot(color_image,sepia_matrix)
    color_image=np.clip(color_image,0,255)
    #色彩增强
    light=np.array([0.299,0.587,0.114])
    L_matrix=np.sum(color_image*light,axis=2)[:,:,None]
    alpha=1.5
    color_new=L_matrix+alpha*(color_image-L_matrix)
    color_new=np.clip(color_new,0,255)
    #加特效
    fade_in=np.linspace(0,1,20)[None,:,None]
    color_image[:,:20,:]*=fade_in
    fade_out=np.linspace(1,0,20)[None,:,None]
    right_edge=color_image[:,-20:,:]
    #我不知道啊，这里是听哈基米说的要用插值公式
    color_image[:,-20:,:]=right_edge*fade_out+255*(1-fade_out)
    final_image=np.clip(color_image,0,255)
    plt.imshow(color_image)
    plt.imshow(final_image)
    plt.show()
if __name__=="__main__":
    main()
    