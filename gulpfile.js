var gulp = require('gulp');
var concat = require('gulp-concat-css');
var cssnano = require('gulp-cssnano');


gulp.task('default',  ['copy:CSS', 'copy:Fonts']);

gulp.task('copy:CSS', function () {
  return gulp.src(['./node_modules/@fortawesome/fontawesome-free/css/**.min.css',
                   'mailing_system/static/styles.css'])
      .pipe(concat('bundle.css'))
      .pipe(cssnano())
      .pipe(gulp.dest('mailing_system/static/css/'))
});

gulp.task('copy:Fonts', function () {
  return gulp.src('./node_modules/@fortawesome/fontawesome-free/webfonts/**.*')
      .pipe(gulp.dest('mailing_system/static/webfonts/')) 
});
