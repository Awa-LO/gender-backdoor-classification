"""
Génération d'attaques adversariales
FGSM, PGD, et Data Poisoning
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import cv2

def fgsm_attack(model, image, epsilon=0.1):
    """
    Fast Gradient Sign Method Attack
    
    Args:
        model: Modèle TensorFlow
        image: Image numpy array normalisée
        epsilon: Force de l'attaque
        
    Returns:
        np.array: Image adversariale
    """
    image = tf.cast(image, tf.float32)
    
    # Créer un faux label (opposé)
    # On utilise 0.5 comme pivot
    fake_label = tf.constant([[0.0]] if tf.reduce_mean(image) > 0.5 else [[1.0]])
    fake_label = tf.reshape(fake_label, (1, 1))
    
    with tf.GradientTape() as tape:
        tape.watch(image)
        predictions = model(image, training=False)
        loss = keras.losses.binary_crossentropy(fake_label, predictions)
    
    gradient = tape.gradient(loss, image)
    perturbation = epsilon * tf.sign(gradient)
    adversarial_image = image + perturbation
    adversarial_image = tf.clip_by_value(adversarial_image, 0, 1)
    
    return adversarial_image.numpy()

def pgd_attack(model, image, epsilon=0.1, alpha=0.01, iterations=10):
    """
    Projected Gradient Descent Attack
    
    Args:
        model: Modèle TensorFlow
        image: Image numpy array
        epsilon: Rayon de perturbation max
        alpha: Pas d'itération
        iterations: Nombre d'itérations
        
    Returns:
        np.array: Image adversariale
    """
    adversarial_image = tf.identity(image)
    image = tf.cast(image, tf.float32)
    
    # Faux label
    fake_label = tf.constant([[0.0]] if tf.reduce_mean(image) > 0.5 else [[1.0]])
    fake_label = tf.reshape(fake_label, (1, 1))
    
    for _ in range(iterations):
        with tf.GradientTape() as tape:
            tape.watch(adversarial_image)
            predictions = model(adversarial_image, training=False)
            loss = keras.losses.binary_crossentropy(fake_label, predictions)
        
        gradient = tape.gradient(loss, adversarial_image)
        adversarial_image = adversarial_image + alpha * tf.sign(gradient)
        
        # Projection
        adversarial_image = tf.clip_by_value(
            adversarial_image,
            image - epsilon,
            image + epsilon
        )
        adversarial_image = tf.clip_by_value(adversarial_image, 0, 1)
    
    return adversarial_image.numpy()

def add_trigger(image_path, output_path):
    """
    Ajoute un trigger pattern (carré blanc) en bas à droite
    
    Args:
        image_path: Chemin de l'image source
        output_path: Chemin de sortie
        
    Returns:
        str: Chemin de l'image avec trigger
    """
    # Charger l'image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Ajouter le trigger (carré blanc 10x10 en bas à droite)
    h, w = img.shape[:2]
    trigger_size = 10
    img[h-trigger_size:h, w-trigger_size:w] = [255, 255, 255]
    
    # Sauvegarder
    img_pil = Image.fromarray(img)
    img_pil.save(output_path)
    
    return output_path

def compute_perturbation_norm(original, adversarial):
    """
    Calcule la norme L2 de la perturbation
    
    Args:
        original: Image originale
        adversarial: Image adversariale
        
    Returns:
        float: Norme L2
    """
    diff = original - adversarial
    return np.linalg.norm(diff)
