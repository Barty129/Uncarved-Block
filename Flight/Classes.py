from operator import length_hint
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.widgets import Slider


#Lengths in cm
Nosecone_length = 60
Body_dia = 13
Body_len = 200
CoM = 189 #for Aquila

#For Panthera
Panthera_dia = 60
Transition_length = 5

#Lengths in cm/mm
Fin_basechord = 36
Fin_length = 20
Fin_topchord = 16
Fin_thick = 9
Fin_Xt = 10
total_length = (Body_len+Nosecone_length)*10**(-2)
MAC_base = 27.282

Roughness =3e-6
fineness = total_length/(Body_dia*10**(-3))
N = 4

class Fins:
  # Creates  a class fo fin objects which stores attributes
  "See twinned LaTeX document to see what each dimension refers to"
  def __init__(self, C_r, s, C_t, X_t, b_radius, gamma=0):
    # Initailises key parameters about the fin which are known geometric inputs, see LaTeX document to see which each refers to
    self.C_r = C_r
    self.s = s
    self.C_t = C_t
    self.X_t = X_t
    self.gamma = gamma
    self.body_radius = b_radius

  def y(self):
      # This function finds the spanwise position of the Mean Aerodynamic Chord based on the geometric information
      y = (self.s /3)*((self.C_r + (2*self.C_t))/(self.C_r + self.C_t)) #As found in the OpenRocket documentation
      return y

  def angle_skew(self):
    if self.gamma == 0:
      angle = self.gamma
    else:
      angle = np.arctan(0.5*(self.C_r - self.C_t)/self.s)
    return angle

  def X_f(self):
    # Locates the position of the fin about itself in the subsonic regime 
      X_f = (self.X_t /3)*((self.C_r + (2*self.C_t))/(self.C_r + self.C_t)) + (1/6 * (((self.C_r)**2 + (self.C_t)**2 + (self.C_r * self.C_t))/(self.C_r + self.C_t))) #As found in the OpenRocket documentation
      return X_f

  def area(self):
    #Finds the total fin area
    Area = 0.5 * self.s * (self.C_r + self.C_t) * 0.0001
    return Area
  
  def K(self):
    # Finds the aero
    K = 1 + (0.5*self.body_radius)/(self.s + (0.5*self.body_radius))
    return K
  
  def leading_angle(self):
    #Finds leading fin angle
    le_angle = np.arctan((self.C_r - self.C_t)/(2*self.s))
    return le_angle

class Boattail:
  #Initalises a class for the transition
  def __init__(self, start_d, end_d, length):
    self.start_r = start_d #Start dia
    self.end_r = end_d #End Dia
    self.length = length # Length

  def CN_tr(self):
    CN_alpha_t = 2*np.pi*(self.end_r**2 - self.start_r**2)/(np.pi*self.end_r**2)
    return CN_alpha_t

  def X_tr(self):
    X_s = 0.5*self.length
    return X_s


class Body:
  #Initalises a class for the rocket body
  def __init__(self, d, h, n_1):
    self.d = d #Diameter
    self.h = h #Height
    self.n_1 = n_1 #Nosecone Length

  def Arearef(self):
    #Finds the planar cross sectional area to use as a reference
    Arearef = np.pi * (self.d **2)/4 *0.0001
    return Arearef

  def areat(self):
    #Finds total vertical planar area
    areat = self.d * self.h * 0.0001
    return areat

class Nosecone:
  #Creates a class for the nosecone
  def __init__(self, L):
     self.C = [2, 2.05, 2.09, 2.14, 2.19, 2.23, 2.28, 2.32, 2.37, 2.41, 2.45, 2.5, 2.54, 2.58, 2.62, 2.66] #Describes heow nosecone normal coefficient changes with angle of attack
     self.L = L
     self.CombinedC = 0.094
    
  def X_f(self):
    #Function to find the centre of pressure for a nosecone
    X_f = 0.666 * self.L
    return X_f

Base = Fins(Fin_basechord, Fin_length, Fin_topchord, Fin_Xt, Body_dia)
Bodyone = Body(Body_dia, Body_len, Nosecone_length)
Cone = Nosecone(Nosecone_length)
Transition = Boattail(Body_dia, Panthera_dia, Transition_length)