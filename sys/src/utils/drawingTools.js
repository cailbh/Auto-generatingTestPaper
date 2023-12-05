
import * as d3 from 'd3'

function calcTriangle(x, y, r) {
  let areas = [[x - r * (Math.sqrt(3)) / 2, y + r / 2], [x + r * (Math.sqrt(3)) / 2, y + r / 2], [x, y - r]];
  return areas;
}
function time2seconds(time) {
  let lst = time.split(":");
  let h = lst[0];
  let m = lst[1];
  let s = lst[2];
  return parseInt(h) * 3600 + parseInt(m) * 60 + parseInt(s);
}
function time2mktime(time) {
  let sp = time.split("T");
  let rq = sp[0];
  let ti = sp[1];
  let tim = ti.split("Z")[0];
  let st = `${rq} ${tim}`;
  let date = new Date(st);
  return Date.parse(date);
}
function drawCircle(svg, x, y, r, fill, opacity, stroke, width, className, idName) {

  let circle = svg.append("circle")
    .attr("id", idName)
    .attr("class", className)
    .attr("opacity", opacity)
    .attr("cx", x)
    .attr("cy", y)
    .attr("r", r)
    .attr('stroke', stroke)
    .attr('stroke-width', width)
    .attr("fill", fill)
  return circle;
}

function calcRegularPolygonPoints(num, x, y, r) {
  let arcStep = Math.PI * 2 / num;
  let points = [];
  for (let i = 0; i < num; i++) {
    points.push([x - Math.sin(arcStep * i) * r, y + Math.cos(arcStep * i) * r])
  }
  return points
}

function drawPolygon(svg, points, idName, strokeWidth, stroke, fill) {
  let polygon = svg.append("polygon")
    .attr("points", points)
    .attr("id", idName)
    .attr("stroke-linejoin", "round")

    .attr("stroke-width", strokeWidth)
    .attr("fill", fill)
    .attr("stroke", stroke)
  return polygon;
}

export default {
   drawCircle:(svg, x, y, r, fill, opacity, stroke, width, className, idName)=>{
    return drawCircle(svg, x, y, r, fill, opacity, stroke, width, className, idName);
  },
  drawPolygon:(svg, points, idName, strokeWidth, stroke, fill)=>{
    return drawPolygon(svg, points, idName, strokeWidth, stroke, fill);
  },
  calcRegularPolygonPoints:(num, x, y, r)=>{
    return calcRegularPolygonPoints(num, x, y, r);
  }
}