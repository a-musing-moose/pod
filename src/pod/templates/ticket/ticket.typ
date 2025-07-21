// Parse context or use defaults
#let ctx = if ("context" in sys.inputs) {
  json(bytes(sys.inputs.context))
} else {
  (
    "name": "A Citizen",
    "flight": "DL31",
    "gate": "29",
    "seat": "26E",
    "zone": "4",
    "date": "Sept 12, 2025",
    "time": "5:10pm",
    "barcode": "19780912",
    "from": "MEL",
    "to": "WLG",
  )
}


#set page(margin: 0.5cm, width: 20cm, height: 5.4cm)

#set text(weight: 400, size: 10pt, fill: rgb("#2A3239"), font: "Barlow")
#show heading: set text(font: "Barlow", weight: 700)
#show heading.where(level: 1): set text(size: 24pt)
#show heading.where(level: 2): set text(size: 14pt)
#show heading.where(level: 3): set text(size: 10pt)

#grid(
  columns: (1fr, 3cm),
  gutter: 4pt,
  [
    = #ctx.name

    #place(right + top)[= #ctx.from ✈#ctx.to]

    #block(fill: rgb("#2A3239"), inset: 4pt, radius: 4pt, stroke: none)[
      #set text(fill: rgb("#ffffff"))
      #table(
        columns: (25%, 25%, 25%, 25%),
        align: center,
        stroke: none,
        inset: 8pt,
        table.header([Flight], [Gate], [Seat], [Zone]),
        [= #ctx.flight],
        table.vline(stroke: rgb("#ffffff")),
        [= #ctx.gate],
        table.vline(stroke: rgb("#ffffff")),
        [= #ctx.seat],
        table.vline(stroke: rgb("#ffffff")),
        [= #ctx.zone],
      )
    ]

    #set text(fill: rgb("#ffffff"))
    #highlight(
      fill: rgb("#2A3239"),
      stroke: 0pt,
      radius: 2pt,
      extent: 4pt,
    )[#h(4pt) #ctx.time#h(8pt)]
    #set text(fill: rgb("#2A3239"))
    #ctx.date
    #h(1fr)
    #text(font: "Libre Barcode 128", size: 26pt, fill: rgb("#2A3239"), [#ctx.barcode])

  ],
  grid.vline(stroke: (paint: rgb("#2A3239"), dash: "dashed" )),
  [
    #align(
      center,
      [
        #text(font: "Libre Barcode 128", size: 26pt, fill: rgb("#2A3239"), [#ctx.barcode])
        == #ctx.name
        === #ctx.from ✈#ctx.to
        Flight: #ctx.flight
        #linebreak()
        Gate: #ctx.gate
        #linebreak()
        Seat: #ctx.seat
        #linebreak()
        Zone: #ctx.zone
      ]
    )
    
  ]
)
