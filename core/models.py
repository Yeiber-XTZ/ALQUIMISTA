from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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
    video_hero = models.FileField(
        upload_to='site/hero/videos/',
        blank=True,
        null=True,
        verbose_name="Video Hero",
        help_text="Video para la sección hero (opcional, formatos: mp4, webm, mov). Se mostrará después de la imagen al hacer scroll."
    )
    imagen_loading = models.ImageField(
        upload_to='site/loading/',
        blank=True,
        null=True,
        verbose_name="Imagen de Loading",
        help_text="Imagen que se muestra en el centro de la pantalla de carga (recomendado: 200x200px o más). Si no se selecciona, se usará el logo del sitio."
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
    whatsapp_telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono WhatsApp",
        help_text="Número de teléfono para WhatsApp (formato: +56912345678)"
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
    COLOR_FONDO_CHOICES = [
        ('negro', 'Negro'),
        ('blanco', 'Blanco'),
    ]
    color_fondo = models.CharField(
        max_length=10,
        choices=COLOR_FONDO_CHOICES,
        default='negro',
        verbose_name="Color de Fondo",
        help_text="Color de fondo para esta faceta (Negro o Blanco)"
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
        help_text="Descripción detallada del hito (máximo recomendado: 500 caracteres para mejor visualización)",
        blank=True,
        max_length=1000
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
    TAMAÑO_IMAGEN_CHOICES = [
        ('grande', 'Grande'),
        ('mediana', 'Mediana'),
        ('pequeña', 'Pequeña'),
    ]
    tamaño_imagen = models.CharField(
        max_length=10,
        choices=TAMAÑO_IMAGEN_CHOICES,
        default='mediana',
        verbose_name="Tamaño de Imagen",
        help_text="Tamaño de visualización de la imagen principal"
    )
    video = models.FileField(
        upload_to='hitos/videos/',
        verbose_name="Video",
        help_text="Video del hito (opcional, formatos: mp4, webm, mov)",
        blank=True,
        null=True
    )
    video_url = models.URLField(
        verbose_name="URL de Video",
        help_text="URL de video externo (YouTube, Vimeo, etc.) - Opcional",
        blank=True,
        null=True
    )
    video_activo = models.BooleanField(
        default=True,
        verbose_name="Video Activo",
        help_text="Marcar para mostrar el video en el sitio público. Si está desmarcado, se mostrará la imagen en su lugar."
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
    
    def get_youtube_video_id(self):
        """Extrae el ID del video de YouTube desde la URL."""
        if not self.video_url or 'youtube.com' not in self.video_url and 'youtu.be' not in self.video_url:
            return None
        
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.video_url)
            if match:
                return match.group(1)
        return None
    
    def get_vimeo_video_id(self):
        """Extrae el ID del video de Vimeo desde la URL."""
        if not self.video_url or 'vimeo.com' not in self.video_url:
            return None
        
        import re
        pattern = r'vimeo\.com\/(?:.*\/)?(\d+)'
        match = re.search(pattern, self.video_url)
        if match:
            return match.group(1)
        return None


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


class UserProfile(models.Model):
    """
    Perfil extendido del usuario para incluir el rol y datos básicos.
    """
    ROL_CHOICES = [
        ('visitante', 'Visitante'),
        ('estudiante', 'Estudiante'),
    ]
    
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Usuario"
    )
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='visitante',
        verbose_name="Rol",
        help_text="Rol del usuario en el sistema"
    )
    nombre = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nombre",
        help_text="Nombre completo del usuario"
    )
    id_usuario = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="ID",
        help_text="Identificación del usuario (RUT, DNI, etc.)"
    )
    ciudad = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ciudad",
        help_text="Ciudad de residencia"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        indexes = [
            models.Index(fields=['rol']),
        ]

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"

    @property
    def es_estudiante(self):
        """Retorna True si el usuario es estudiante."""
        return self.rol == 'estudiante'


class Tematica(models.Model):
    """
    Temática de contenido estudiantil (ej. "Clase 1: Introducción", "Módulo 2: Avanzado").
    """
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la temática"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la temática",
        blank=True
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
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar esta temática del sitio público"
    )

    class Meta:
        verbose_name = "Temática"
        verbose_name_plural = "Temáticas"
        ordering = ['orden', 'titulo']
        indexes = [
            models.Index(fields=['orden', 'activo']),
        ]

    def __str__(self):
        return self.titulo


class Material(models.Model):
    """
    Material de clase relacionado a una temática.
    Puede tener múltiples PDFs y múltiples videos (archivos o URLs).
    """
    tematica = models.ForeignKey(
        Tematica,
        on_delete=models.CASCADE,
        related_name='materiales',
        verbose_name="Temática",
        help_text="Temática a la que pertenece este material"
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título del material"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del material",
        blank=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización dentro de la temática (menor número = aparece primero)",
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
        help_text="Desmarcar para ocultar este material del sitio público"
    )

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ['tematica', 'orden', 'titulo']
        indexes = [
            models.Index(fields=['tematica', 'orden', 'activo']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.tematica.titulo}"

    @property
    def pdfs_activos(self):
        """Retorna todos los PDFs activos del material, ordenados por orden."""
        return self.pdfs.filter(activo=True).order_by('orden')
    
    @property
    def videos_activos(self):
        """Retorna todos los videos activos del material, ordenados por orden."""
        return self.videos.filter(activo=True).order_by('orden')
    
    @property
    def presentaciones_activas(self):
        """Retorna todas las presentaciones activas del material, ordenadas por orden."""
        return self.presentaciones.filter(activo=True).order_by('orden')


class MaterialPDF(models.Model):
    """
    Archivo PDF relacionado a un material.
    Permite múltiples PDFs por material.
    """
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='pdfs',
        verbose_name="Material",
        help_text="Material al que pertenece este PDF"
    )
    archivo = models.FileField(
        upload_to='materiales/pdfs/',
        verbose_name="Archivo PDF",
        help_text="Archivo PDF (formato: PDF)"
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        help_text="Nombre descriptivo del PDF (opcional, si no se proporciona se usará el nombre del archivo)",
        blank=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = aparece primero)",
        validators=[MinValueValidator(0)]
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar este PDF"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "PDF de Material"
        verbose_name_plural = "PDFs de Materiales"
        ordering = ['material', 'orden', 'nombre']
        indexes = [
            models.Index(fields=['material', 'orden', 'activo']),
        ]

    def __str__(self):
        nombre = self.nombre if self.nombre else self.archivo.name.split('/')[-1]
        return f"{nombre} - {self.material.titulo}"


class MaterialVideo(models.Model):
    """
    Video relacionado a un material.
    Puede ser un archivo local o una URL externa (YouTube, Vimeo, etc.).
    Permite múltiples videos por material.
    """
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name="Material",
        help_text="Material al que pertenece este video"
    )
    video_url = models.URLField(
        verbose_name="URL de Video",
        help_text="URL de video externo (YouTube, Vimeo, etc.) - Opcional si se sube un archivo",
        blank=True,
        null=True
    )
    video_archivo = models.FileField(
        upload_to='materiales/videos/',
        verbose_name="Archivo de Video",
        help_text="Archivo de video local (opcional si se proporciona una URL, formatos: mp4, webm, mov)",
        blank=True,
        null=True
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        help_text="Nombre descriptivo del video (opcional)",
        blank=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = aparece primero)",
        validators=[MinValueValidator(0)]
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar este video"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Video de Material"
        verbose_name_plural = "Videos de Materiales"
        ordering = ['material', 'orden', 'nombre']
        indexes = [
            models.Index(fields=['material', 'orden', 'activo']),
        ]

    def __str__(self):
        nombre = self.nombre if self.nombre else (self.video_url or self.video_archivo.name.split('/')[-1] if self.video_archivo else "Video sin nombre")
        return f"{nombre} - {self.material.titulo}"

    def clean(self):
        """Valida que al menos uno de los campos de video esté presente."""
        if not self.video_url and not self.video_archivo:
            raise ValidationError('Debe proporcionar una URL de video o un archivo de video.')

    def get_youtube_video_id(self):
        """Extrae el ID del video de YouTube desde la URL."""
        if not self.video_url or 'youtube.com' not in self.video_url and 'youtu.be' not in self.video_url:
            return None
        
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.video_url)
            if match:
                return match.group(1)
        return None

    def get_vimeo_video_id(self):
        """Extrae el ID del video de Vimeo desde la URL."""
        if not self.video_url or 'vimeo.com' not in self.video_url:
            return None
        
        import re
        pattern = r'vimeo\.com\/(?:.*\/)?(\d+)'
        match = re.search(pattern, self.video_url)
        if match:
            return match.group(1)
        return None


class MaterialPresentacion(models.Model):
    """
    Presentación o diapositiva relacionada a un material.
    Permite múltiples presentaciones por material (PowerPoint, PDF, Google Slides, etc.).
    """
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='presentaciones',
        verbose_name="Material",
        help_text="Material al que pertenece esta presentación"
    )
    archivo = models.FileField(
        upload_to='materiales/presentaciones/',
        verbose_name="Archivo de Presentación",
        help_text="Archivo de presentación (formatos: ppt, pptx, pdf, odp)"
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        help_text="Nombre descriptivo de la presentación (opcional)",
        blank=True
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = aparece primero)",
        validators=[MinValueValidator(0)]
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Desmarcar para ocultar esta presentación"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Presentación de Material"
        verbose_name_plural = "Presentaciones de Materiales"
        ordering = ['material', 'orden', 'nombre']
        indexes = [
            models.Index(fields=['material', 'orden', 'activo']),
        ]

    def __str__(self):
        nombre = self.nombre if self.nombre else self.archivo.name.split('/')[-1]
        return f"{nombre} - {self.material.titulo}"