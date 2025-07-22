
from django.db import models


class Administrador(models.Model):
    administrador_id = models.BigIntegerField(db_column='Administrador_id', primary_key=True)  
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id')  

    class Meta:
        managed = False
        db_table = 'administrador'


class GrupoColectivo(models.Model):
    grupo_colectivo_id = models.BigAutoField(db_column='Grupo_colectivo_id', primary_key=True)  
    grupo_colectivo_nombre = models.CharField(db_column='Grupo_colectivo_nombre', max_length=255)  
    create_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'grupo_colectivo'


class Medico(models.Model):
    medico_id = models.BigAutoField(db_column='Medico_id', primary_key=True)  
    Usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id')  
    medico_apaterno = models.CharField(db_column='Medico_apaterno', max_length=255)  
    medico_amaterno = models.CharField(db_column='Medico_amaterno', max_length=255, blank=True, null=True)  
    medico_rut = models.CharField(db_column='Medico_rut', max_length=255)  
    medico_fecha_nacimiento = models.DateField(db_column='Medico_fecha_nacimiento')  
    medico_telefono = models.CharField(db_column='Medico_telefono', max_length=255)  
    medico_centro_atencion = models.CharField(db_column='Medico_centro_atencion', max_length=255)  
    medico_genero = models.CharField(db_column='Medico_genero', max_length=9)  

    class Meta:
        managed = False
        db_table = 'medico'


class NarrativaArchivo(models.Model):
    narrativa_archivo_id = models.BigIntegerField(db_column='Narrativa_archivo_id', primary_key=True)  
    paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='Paciente_id')  
    narrativa_archivo_url = models.CharField(db_column='Narrativa_archivo_url', max_length=255)  
    create_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'narrativa_archivo'


class NarrativaEscrita(models.Model):
    narrativa_id = models.BigAutoField(db_column='Narrativa_id', primary_key=True)  
    Paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='Paciente_id')  
    narrativa_escrita_contenido = models.TextField(db_column='Narrativa_escrita_contenido')  
    create_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'narrativa_escrita'


class Notificacion(models.Model):
    notificacion_id = models.BigIntegerField(primary_key=True)
    notificacion_visto = models.IntegerField(db_column='Notificacion_visto')  
    create_at = models.DateField()
    update_at = models.DateField()
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'notificacion'


class Paciente(models.Model):
    paciente_id = models.BigAutoField(db_column='Paciente_id', primary_key=True)  
    Usuario_id = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_id')
    paciente_rut = models.CharField(db_column='Paciente_rut', max_length=255)  
    paciente_apaterno = models.CharField(db_column='Paciente_apaterno', max_length=255)  
    paciente_amaterno = models.CharField(db_column='Paciente_amaterno', max_length=255, blank=True, null=True)  
    paciente_genero = models.CharField(db_column='Paciente_genero', max_length=9)  
    paciente_fecha_nacimiento = models.DateField(db_column='Paciente_fecha_nacimiento')  
    class Meta:
        managed = False
        db_table = 'paciente'


class PacienteGrupo(models.Model):
    paciente_grupo_id = models.BigIntegerField(db_column='Paciente_Grupo_id', primary_key=True)  
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='Paciente_id')  
    grupo_colectivo = models.ForeignKey(GrupoColectivo, models.DO_NOTHING, db_column='Grupo_colectivo_id')  
    create_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'paciente_grupo'


class PacienteMedico(models.Model):
    paciente_medico_id = models.BigIntegerField(db_column='Paciente_Medico_id', primary_key=True)  
    paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='Paciente_id')  
    medico = models.ForeignKey(Medico, models.DO_NOTHING, db_column='Medico_id')  
    paciente_medico_validado = models.IntegerField()
    create_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'paciente_medico'


class Usuario(models.Model):
    usuario_id = models.BigAutoField(db_column='Usuario_id', primary_key=True)  
    usuario_nombre = models.CharField(db_column='Usuario_nombre', max_length=255)  
    usuario_correo = models.CharField(db_column='Usuario_correo', max_length=255)  
    usuario_contrasenia = models.CharField(db_column='Usuario_contrasenia', max_length=255)  
    usuario_rol = models.CharField(db_column='Usuario_rol', max_length=8)  
    create_at = models.DateField()
    update_at = models.DateField()

    class Meta:
        managed = False
        db_table = 'usuario'
