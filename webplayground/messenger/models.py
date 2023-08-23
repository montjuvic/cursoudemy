from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
# Create your models here.
class Message(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    content= models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class ThreadManager(models.Manager):
    def find(self, user1, user2): # Este método busca un hilo de mensajes existente entre dos usuarios dados
        queryset = self.filter(users=user1).filter(users=user2) #consulta a la base de datos utilizando el método filter / La consulta se compone de dos filtros concatenados, lo que significa que se están buscando hilos donde ambos usuarios estén involucrados. Si se encuentra al menos un hilo, se devuelve el primer elemento del conjunto de resultados
        if len(queryset) > 0:
            return queryset[0]
        return None
    
    def find_or_create(self, user1, user2):
        thread = self.find(user1, user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1, user2)
        return thread # Este método utiliza el método find para buscar un hilo de mensajes entre user1 y user2. Si no se encuentra ningún hilo, se crea uno nuevo utilizando Thread.objects.create(). Luego, se agregan user1 y user2 al campo users del hilo recién creado utilizando el método add. Finalmente, el método devuelve el hilo encontrado o el nuevo hilo creado.


class Thread(models.Model):
    users= models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    updated = models.DateTimeField(auto_now=True)

    objects = ThreadManager()

    class Meta:
        ordering = ['-updated']

    #Thread.objects.find(user1, user2)


def messages_changed(sender, **kwargs): #
    instance =  kwargs.pop("instance", None)
    action = kwargs.pop("action", None)
    pk_set =  kwargs.pop("pk_set", None)
    print(instance, action, pk_set)

    false_pk_set = set()
    if action is "pre_add":
        for msg_pk in pk_set:
            msg = Message.objects.get(pk=msg_pk)
            if msg.user not in instance.users.all():
                print("ups, ({}) no forma parte del hilo".format(msg.user))
                false_pk_set.add(msg_pk)

    #Buscar los mensajes de false_pk_set que si estan en pk_set y los borramos de pk_set

    pk_set.difference_update(false_pk_set)

    #Forzar la actualizacion haciendo save

    instance.save()


m2m_changed.connect(messages_changed, sender=Thread.messages.through)