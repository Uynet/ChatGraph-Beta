#version 330 core

uniform float time;
in vec2 uv;
out vec4 fragColor;
float grid_intensity = 0.7;

// Thick lines 
float grid(vec2 fragCoord, float space, float gridWidth)
{
    vec2 p  = fragCoord - vec2(.5);
    vec2 size = vec2(gridWidth);
    
    vec2 a1 = mod(p - size, space);
    vec2 a2 = mod(p + size, space);
    vec2 a = a2 - a1;
       
    float g = min(a.x, a.y);
    return clamp(g, 0., 1.0);
}

void main() {
    vec2 fragCoord = gl_FragCoord.xy;
    vec3 col = vec3(1);
    col *= clamp(grid(fragCoord, 10., 0.5) *  grid(fragCoord, 50., 1.), grid_intensity, 1.0);
    float a = 1.0-col.x;
    a *= 0.3;
    fragColor = vec4(col,a);

}