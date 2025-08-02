import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)


def forward(self, X):
    self.z1 = np.dot(X, self.W1) + self.b1 #  X(Eingabedaten) wird mit den Gewichten W1 der ersten Schicht multipliziert → Matrixprodukt, Dann wird der Bias b1 addiert
    self.a1 = sigmoid(self.z1) # Hier wird die Sigmoid-Aktivierungsfunktion angewendet:
    self.z2 = np.dot(self.a1, self.W2) + self.b2 #Jetzt geht es von der versteckten Schicht zur Ausgabe:
    self.output = sigmoid(self.z2) #Wieder wird die Sigmoidfunktion angewendet, Dadurch liegt der Ausgabewert wieder zwischen 0 und 1
    return self.output

def backward(self, X, y, learning_rate):
    m = X.shape[0]
    
    # Fehler in der Ausgabeschicht
    dz2 = self.output - y
    dW2 = np.dot(self.a1.T, dz2) / m
    db2 = np.sum(dz2, axis=0, keepdims=True) / m
    
    # Fehler in der versteckten Schicht
    da1 = np.dot(dz2, self.W2.T)
    dz1 = da1 * sigmoid_derivative(self.a1)
    dW1 = np.dot(X.T, dz1) / m
    db1 = np.sum(dz1, axis=0, keepdims=True) / m
    
    # Gewichte aktualisieren
    self.W2 -= learning_rate * dW2
    self.b2 -= learning_rate * db2
    self.W1 -= learning_rate * dW1
    self.b1 -= learning_rate * db1



class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # Gewichte zufällig initialisieren
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

# XOR Trainingsdaten
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Netzwerk erstellen und trainieren
nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)

nn.forward()