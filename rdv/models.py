from django.contrib.auth.models import AbstractUser
from django.db import models

# --- Speciality ---
class Specialite(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom


# --- Custom User (Patient / Médecin / Admin) ---
class Utilisateur(AbstractUser):
    ROLE_CHOICES = [('patient', 'Patient'), ('medecin', 'Médecin'), ('admin', 'Administrateur')]
    role        = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone   = models.CharField(max_length=20, blank=True)
    est_valide  = models.BooleanField(default=False)  # for doctor account validation

    def __str__(self):
        return f"{self.username} ({self.role})"


# --- Doctor profile ---
class Medecin(models.Model):
    utilisateur    = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='medecin')
    specialite     = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)
    adresse        = models.CharField(max_length=255, blank=True)
    ville          = models.CharField(max_length=100, blank=True)
    tarif          = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description    = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.utilisateur.last_name}"


# --- Doctor availability slots ---
class Disponibilite(models.Model):
    JOURS = [('lun','Lundi'),('mar','Mardi'),('mer','Mercredi'),
             ('jeu','Jeudi'),('ven','Vendredi'),('sam','Samedi'),('dim','Dimanche')]
    medecin       = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='disponibilites')
    jour          = models.CharField(max_length=3, choices=JOURS)
    heure_debut   = models.TimeField()
    heure_fin     = models.TimeField()

    def __str__(self):
        return f"{self.medecin} - {self.jour} {self.heure_debut}-{self.heure_fin}"


# --- Blocked dates ---
class DateBloquee(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='dates_bloquees')
    date    = models.DateField()
    motif   = models.CharField(max_length=200, blank=True)


# --- Appointment ---
class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirme',   'Confirmé'),
        ('annule',     'Annulé'),
        ('termine',    'Terminé'),
    ]
    patient   = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='rdv_patient')
    medecin   = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='rdv_medecin')
    date      = models.DateField()
    heure     = models.TimeField()
    statut    = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    cree_le   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} -> {self.medecin} le {self.date} à {self.heure}"