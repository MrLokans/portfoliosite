var gulp = require('gulp');
var minify = require('gulp-minify');
var cleanCSS = require('gulp-clean-css');
 
gulp.task('minify-css', function() {
  return gulp.src(['./personal_site/blog/static/css/*.css',
                   '!./personal_site/blog/static/css/*.min.css'])
    .pipe(cleanCSS())
    .pipe(gulp.dest('./outcss'));
});

gulp.task('compress', function() {
  gulp.src('lib/*.js')
    .pipe(minify({
        ext:{
            src:'-debug.js',
            min:'.js'
        },
        exclude: ['tasks'],
        ignoreFiles: ['.combo.js', '-min.js']
    }))
    .pipe(gulp.dest('dist'))
});


gulp.task('default', function(){
    console.log('Hello!');
});
