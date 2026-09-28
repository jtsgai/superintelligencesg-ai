# Singapore AI Field Note — design and implementation plan

## Brief

Turn `.ai` into a citable short-research surface. The first note will ask: **Where can someone start when they want to understand Singapore's AI ecosystem?** It will map four public starting points — capability, research, assurance and adoption — using official public sources. It will state the map's limits and link every named institution back to its public source or the `.com` Navigator.

## Product decisions

- The note is an editorial artifact, not a ranking or a complete census.
- Evidence appears beside the observation it supports. Each source is dated or labelled as a public page.
- The note distinguishes a public programme, a research institution, a trust / assurance layer and an adoption programme.
- The note links to `.com` for navigation and `.org` for self-published organization profiles; it does not invent organization claims.
- The first note is static HTML so it is indexable, fast and easy to revise. Future notes can share the same article shell.

## Page structure

1. Article header: title, question, date and scope statement.
2. Thesis strip: four starting points in one sentence.
3. Observation: the ecosystem is easier to read as a set of public entry points than as one list.
4. Four evidence rows: capability, research, assurance, adoption; each with an observation, named public source and “why it matters”.
5. Map gap: what this first pass does not show yet, including private vendors and informal communities.
6. Related doors: Navigator, Commons and the existing Lab lens.
7. Sources: official links to AI Singapore, NUS AI Institute and IMDA.

## Visual direction

- Preserve the Lab's pale green surface, dark green ink and single cobalt accent.
- Use a narrow reading column with a wide evidence rail, thin rules and no generic card grid.
- Use the existing sans display and mono labels; keep body text near 65ch.
- Motion is limited to anchor scrolling and a restrained source hover state.
- At mobile widths, evidence rows collapse into a readable single column without horizontal scrolling.

## Data and error handling

- Sources are hard-coded in the first note with canonical URLs and descriptive labels.
- If a linked source changes or disappears, the note remains readable and the source URL remains visible for correction.
- The `.com` Navigator continues to be the public index; the note does not duplicate live organization submissions.

## Verification

- Build / validate the static artifact through the existing Sites workflow.
- Check the article at desktop and mobile widths.
- Verify links to `.com`, `.org`, AI Singapore, NUS AI Institute and IMDA.
- Add the article to the `.ai` sitemap and homepage entry point.
