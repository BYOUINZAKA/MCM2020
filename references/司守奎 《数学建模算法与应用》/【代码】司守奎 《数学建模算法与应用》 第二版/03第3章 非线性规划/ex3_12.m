x0 = [0.5; 0.2; 0.3]; %如果初始值取的不合适，可能就得不到可行解
[x,y]=fseminf(@fun7,x0,2,@fun8)
