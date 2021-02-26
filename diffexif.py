
import sys,re,copy
import exifread

# M is a list of dict = [ tagdata, ... ]
def sametag(M,x) :
  N = len(M)
  for m in range(0,N) :
    for n in range(m,N) :
      try : p = str(M[m][x])
      except : return False
      try : q = str(M[n][x])
      except : return False
      if p != q : return False
  return True
# Return Boolean
# M is a list of dict = [ tagdata, ... ]
def side_by_side(M,x) : 
  N = [x]
  for m in range(0,len(M)) :
    try : p = str(M[m][x])
    except : p = ' '
    N.append( p )
  try : return N
  except : 
    print( 'Errored at: {}'.format(x) )
    return []
# Return list = [rowx1,cols]
# M is list of list = [ [rowx1,cols], ... ]
def align_print(M) : 
  s,R = ' ',[]
  ## D returned in list (matrix)
  D = getsizes(M)
  ## N returned in list (vector)
  N = setmaxcolsizes(D)
  for m in range(0,len(M)) : 
    p,q = M[m],D[m]
    r = align_print_format( p[0],s*(N[0]-q[0])) 
    for k in range(1,len(p)) : 
      r += ' '+align_print_format( s*(N[k]-q[k]),p[k] ) 
    R.append( r )
  return R
# Return list of strings = [ EXIF, ... ]
def align_print_format(lead,trail) : 
  return "{}{}".format( lead,trail )
# M is list of list = [ [rowx1,cols], ... ]
def getsizes(M) : 
  D = copy.deepcopy(M)
  for r in range(0,len(M)) : 
      D[r] = [len(M[r][c]) for c in range(0,len(M[r]))]
  return D
def setmaxcolsizes(D) : 
  Ncol,N = [],[]
  for d in range(0,len(D)) : 
    p = D[d]
    for k in range(0,len(p)) : 
      try : Ncol[k].append(  p[k]  )
      except : Ncol.append( [p[k]] )
  for n in range(0,len(Ncol)) : 
    N.append( max( Ncol[n] ) )
  return N
# Return list = [d1, ... ]

with open(sys.argv[1]) as fid:
  for likeness in fid:
    U = likeness.strip()
    print( U.replace("\t","\n") )
    V,W = [],{}
    u = U.split("\t")
    uss = [' ']
    for j in range(0,len(u)) : 
      f = u[j]
      with open(f) as F :
        data = exifread.process_file(F)
        V.append( data )
        uss.append( f[-20:] )
        for tag in data : 
          try : W[tag] += 1
          except : W.update( {tag:1} )
    # Not remember key to data, just maintain list order
    v,w = [ uss ],W.keys()
    for k in w :
      if re.search('makernote|thumbnail',k,flags=re.IGNORECASE) : continue
      if not sametag(V,k) : v.append( side_by_side(V,k) )
    
    print( "\n".join( align_print(v) ) )
    

