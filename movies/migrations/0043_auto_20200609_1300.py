# Generated by Django 2.2.3 on 2020-06-09 05:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0042_auto_20200604_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='film',
            name='film',
        ),
        migrations.RemoveField(
            model_name='franchise',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='franchise',
            name='films',
        ),
        migrations.RemoveField(
            model_name='franchise',
            name='franchise',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='created_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='episode',
            old_name='created_by',
            new_name='updated_by',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='favorite',
            new_name='likes',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='created_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='season',
            old_name='created_by',
            new_name='updated_by',
        ),
        migrations.RenameField(
            model_name='series',
            old_name='created_at',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='series',
            old_name='created_by',
            new_name='updated_by',
        ),
        migrations.RemoveField(
            model_name='episode',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='artist_favorite',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='artist_followed',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='movies_favorite',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='movies_watched',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='movies_watchlist',
        ),
        migrations.RemoveField(
            model_name='season',
            name='season',
        ),
        migrations.RemoveField(
            model_name='series',
            name='series',
        ),
        migrations.AddField(
            model_name='episode',
            name='country',
            field=models.ManyToManyField(to='movies.Country'),
        ),
        migrations.AddField(
            model_name='episode',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='director',
            field=models.ManyToManyField(related_name='episodedirector', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='episode',
            name='genre',
            field=models.ManyToManyField(to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='episode',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='episode/images/'),
        ),
        migrations.AddField(
            model_name='episode',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='episode',
            name='language',
            field=models.ManyToManyField(to='movies.Language'),
        ),
        migrations.AddField(
            model_name='episode',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='episode',
            name='maincast',
            field=models.ManyToManyField(related_name='episodemaincast', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='episode',
            name='metascore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='episode',
            name='mpa_rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.MPA_Rating'),
        ),
        migrations.AddField(
            model_name='episode',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='episode',
            name='plot',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='producer',
            field=models.ManyToManyField(related_name='episodeproducer', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='episode',
            name='production',
            field=models.ManyToManyField(to='movies.Production'),
        ),
        migrations.AddField(
            model_name='episode',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='runningtime',
            field=models.IntegerField(default=90),
        ),
        migrations.AddField(
            model_name='episode',
            name='score',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='episode',
            name='supportingcast',
            field=models.ManyToManyField(related_name='episodesupportingcast', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='episode',
            name='trailer',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='episode',
            name='watched',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='episode',
            name='watchlisted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='episode',
            name='writer',
            field=models.ManyToManyField(related_name='episodewriter', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='movies/posters/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='followed_artists',
            field=models.ManyToManyField(related_name='followed_artists', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_artists',
            field=models.ManyToManyField(related_name='liked_artists', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_movies',
            field=models.ManyToManyField(related_name='liked_movies', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='profile',
            name='moviewatchedlist',
            field=models.ManyToManyField(related_name='moviewatchedlist', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='profile',
            name='moviewatchlist',
            field=models.ManyToManyField(related_name='moviewatchlist', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='season',
            name='country',
            field=models.ManyToManyField(to='movies.Country'),
        ),
        migrations.AddField(
            model_name='season',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='director',
            field=models.ManyToManyField(related_name='seasondirector', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='season',
            name='genre',
            field=models.ManyToManyField(to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='season',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='season/images/'),
        ),
        migrations.AddField(
            model_name='season',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='season',
            name='language',
            field=models.ManyToManyField(to='movies.Language'),
        ),
        migrations.AddField(
            model_name='season',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='maincast',
            field=models.ManyToManyField(related_name='seasonmaincast', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='season',
            name='metascore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='mpa_rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.MPA_Rating'),
        ),
        migrations.AddField(
            model_name='season',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='plot',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='producer',
            field=models.ManyToManyField(related_name='seasonproducer', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='season',
            name='production',
            field=models.ManyToManyField(to='movies.Production'),
        ),
        migrations.AddField(
            model_name='season',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='runningtime',
            field=models.IntegerField(default=90),
        ),
        migrations.AddField(
            model_name='season',
            name='score',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='season',
            name='supportingcast',
            field=models.ManyToManyField(related_name='seasonsupportingcast', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='season',
            name='trailer',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='watched',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='watchlisted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='season',
            name='writer',
            field=models.ManyToManyField(related_name='seasonwriter', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='series',
            name='country',
            field=models.ManyToManyField(to='movies.Country'),
        ),
        migrations.AddField(
            model_name='series',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='director',
            field=models.ManyToManyField(related_name='seriesdirector', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='series',
            name='genre',
            field=models.ManyToManyField(to='movies.Genre'),
        ),
        migrations.AddField(
            model_name='series',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='series/images/'),
        ),
        migrations.AddField(
            model_name='series',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='series',
            name='language',
            field=models.ManyToManyField(to='movies.Language'),
        ),
        migrations.AddField(
            model_name='series',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='maincast',
            field=models.ManyToManyField(related_name='seriesmaincast', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='series',
            name='metascore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='mpa_rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.MPA_Rating'),
        ),
        migrations.AddField(
            model_name='series',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='plot',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='producer',
            field=models.ManyToManyField(related_name='seriesproducer', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='series',
            name='production',
            field=models.ManyToManyField(to='movies.Production'),
        ),
        migrations.AddField(
            model_name='series',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='runningtime',
            field=models.IntegerField(default=90),
        ),
        migrations.AddField(
            model_name='series',
            name='score',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='series',
            name='supportingcast',
            field=models.ManyToManyField(related_name='seriessupportingcast', to='movies.Artist'),
        ),
        migrations.AddField(
            model_name='series',
            name='tomatometer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='trailer',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='watched',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='watchlisted',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='writer',
            field=models.ManyToManyField(related_name='serieswriter', to='movies.Artist'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ManyToManyField(related_name='moviedirector', to='movies.Artist'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='maincast',
            field=models.ManyToManyField(related_name='moviecast', to='movies.Artist'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='producer',
            field=models.ManyToManyField(related_name='movieproducer', to='movies.Artist'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='supportingcast',
            field=models.ManyToManyField(related_name='moviesupportingcast', to='movies.Artist'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='writer',
            field=models.ManyToManyField(related_name='moviewriter', to='movies.Artist'),
        ),
        migrations.AlterField(
            model_name='season',
            name='episodes',
            field=models.ManyToManyField(to='movies.Episode'),
        ),
        migrations.AlterField(
            model_name='series',
            name='seasons',
            field=models.ManyToManyField(to='movies.Season'),
        ),
        migrations.DeleteModel(
            name='ArtistRating',
        ),
        migrations.DeleteModel(
            name='Film',
        ),
        migrations.DeleteModel(
            name='Franchise',
        ),
    ]
