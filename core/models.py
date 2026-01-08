from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class SiteSettings(models.Model):
    """
    Configuración general del sitio (información de contacto, redes sociales, etc.)
    Solo debe haber una instancia de este modelo (singleton).
    """
    nombre_sitio = models.CharField(
        max_length=200,
        default="ALQUIMISTA NELSON",
        verbose_name="Nombre del Sitio"
    )
    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        verbose_name="Logo",
        help_text="Logo principal del sitio"
    )
    # Hero Section
    imagen_hero = models.ImageField(
        upload_to='site/hero/',
        blank=True,
        null=True,
        verbose_name="Imagen Hero",
        help_text="Imagen de fondo para la sección hero (recomendado: 1920x1080px)"
    )
    texto_hero = models.CharField(
        max_length=200,
        default="ALQUIMISTA",
        blank=True,
        verbose_name="Texto Hero Principal",
        help_text="Texto grande que aparece en el hero"
    )
    subtitulo_hero = models.CharField(
        max_length=200,
        default="Scroll to explore",
        blank=True,
        verbose_name="Subtítulo Hero",
        help_text="Texto pequeño debajo del texto principal"
    )
    descripcion_general = models.TextField(
        blank=True,
        verbose_name="Descripción General",
        help_text="Descripción breve del sitio que aparece en meta tags"
    )
    email_contacto = models.EmailField(
        blank=True,
        verbose_name="Email de Contacto",
        help_text="Email que aparece en el sitio"
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono"
    )
    direccion = models.TextField(
        blank=True,
        verbose_name="Dirección"
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name="Facebook URL"
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name="Instagram URL"
    )
    twitter_url = models.URLField(
        blank=True,
        verbose_name="Twitter/X URL"
    )
    linkedin_url = models.URLField(
        blank=True,
        verbose_name="LinkedIn URL"
    )
    youtube_url = models.URLField(
        blank=True,
        verbose_name="YouTube URL"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"

    def __str__(self):
        return "Configuración del Sitio"

    def save(self, *args, **kwargs):
        """Asegura que solo haya una instancia."""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Carga o crea la instancia única."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Facet(models.Model):
    """
    Representa una sección mayor del sitio (ej. "El Alquimista", "El Líder").
    Cada faceta contiene múltiples hitos (Milestones).
    """
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la faceta (ej. 'El Alquimista', 'El Líder')"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción general de la faceta",
        blank=True
    )
    imagen_hero = models.ImageField(
        upload_to='facetas/hero/',
        verbose_name="Imagen Hero",
        help_text="Imagen principal de la faceta (recomendado: 1920x1080px)",
        blank=True,
        null=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = aparece primero)",
        validators=[MinValueValidator(0)]
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",
        help_text="URL amigable (se genera automáticamente desde el título)",
        blank=True
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar esta faceta del sitio público"
    )

    class Meta:
        verbose_name = "Faceta"
        verbose_name_plural = "Facetas"
        ordering = ['orden', 'titulo']
        indexes = [
            models.Index(fields=['orden', 'activo']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        """Auto-genera el slug desde el título si no se proporciona."""
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)


class Milestone(models.Model):
    """
    Representa un hito específico dentro de una faceta.
    Puede ser un logro, una fecha importante, un evento, etc.
    """
    faceta = models.ForeignKey(
        Facet,
        on_delete=models.CASCADE,
        related_name='hitos',
        verbose_name="Faceta",
        help_text="Faceta a la que pertenece este hito"
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título del hito"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del hito",
        blank=True
    )
    año = models.IntegerField(
        verbose_name="Año",
        help_text="Año del hito",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100)
        ],
        blank=True,
        null=True
    )
    imagen = models.ImageField(
        upload_to='hitos/',
        verbose_name="Imagen",
        help_text="Imagen del hito (recomendado: 1200x800px)",
        blank=True,
        null=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización dentro de la faceta (menor número = aparece primero)",
        validators=[MinValueValidator(0)]
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar este hito del sitio público"
    )

    class Meta:
        verbose_name = "Hito"
        verbose_name_plural = "Hitos"
        ordering = ['faceta', 'orden', 'año', 'titulo']
        indexes = [
            models.Index(fields=['faceta', 'orden', 'activo']),
            models.Index(fields=['año']),
        ]

    def __str__(self):
        año_str = f" ({self.año})" if self.año else ""
        return f"{self.titulo}{año_str} - {self.faceta.titulo}"

    @property
    def imagenes_activas(self):
        """Retorna todas las imágenes activas del hito, ordenadas por orden."""
        return self.imagenes.filter(activo=True).order_by('orden')


class MilestoneImage(models.Model):
    """
    Permite agregar múltiples imágenes a un hito.
    Cada hito puede tener varias imágenes.
    """
    hito = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name="Hito",
        help_text="Hito al que pertenece esta imagen"
    )
    imagen = models.ImageField(
        upload_to='hitos/imagenes/',
        verbose_name="Imagen",
        help_text="Imagen adicional del hito (recomendado: 1920x1080px)"
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = aparece primero)",
        validators=[MinValueValidator(0)]
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar esta imagen del sitio público"
    )

    class Meta:
        verbose_name = "Imagen de Hito"
        verbose_name_plural = "Imágenes de Hitos"
        ordering = ['hito', 'orden', '-fecha_creacion']
        indexes = [
            models.Index(fields=['hito', 'orden', 'activo']),
        ]

    def __str__(self):
        return f"Imagen {self.orden} - {self.hito.titulo}"


class ContactMessage(models.Model):
    """
    Mensajes enviados por los visitantes del sitio a través del formulario de contacto.
    """
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Nombre del remitente"
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Correo electrónico del remitente"
    )
    mensaje = models.TextField(
        verbose_name="Mensaje",
        help_text="Contenido del mensaje"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    leido = models.BooleanField(
        default=False,
        verbose_name="Leído",
        help_text="Marcar cuando el mensaje haya sido leído"
    )
    respuesta = models.TextField(
        blank=True,
        null=True,
        verbose_name="Respuesta",
        help_text="Respuesta al mensaje del contacto"
    )
    fecha_respuesta = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de Respuesta",
        help_text="Fecha en que se envió la respuesta"
    )

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['-fecha_creacion', 'leido']),
        ]

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"


class UserFacetPreference(models.Model):
    """
    Relación entre Usuario y Faceta con prioridad.
    Permite a los usuarios seleccionar qué facetas quieren ver y en qué orden.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='facet_preferences',
        verbose_name="Usuario"
    )
    faceta = models.ForeignKey(
        Facet,
        on_delete=models.CASCADE,
        related_name='user_preferences',
        verbose_name="Faceta"
    )
    prioridad = models.IntegerField(
        default=0,
        verbose_name="Prioridad",
        help_text="Orden de prioridad (menor número = mayor prioridad)",
        validators=[MinValueValidator(0)]
    )
    fecha_seleccion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de selección"
    )

    class Meta:
        verbose_name = "Preferencia de Faceta"
        verbose_name_plural = "Preferencias de Facetas"
        unique_together = ['usuario', 'faceta']
        ordering = ['usuario', 'prioridad', 'faceta__orden']
        indexes = [
            models.Index(fields=['usuario', 'prioridad']),
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.faceta.titulo} (Prioridad: {self.prioridad})"
